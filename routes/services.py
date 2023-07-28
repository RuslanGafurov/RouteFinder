from re import findall

from cities.models import City
from routes.forms import RouteModelForm
from trains.models import Train


def get_routes(form) -> dict:
    """ Функция получения всех возможных маршрутов.
    Итоговый список передается в контроллер route_search_view """

    context = {'form': form}
    trains = Train.objects.all().select_related('from_city', 'to_city')  # ___________ Все поезда
    graph = get_graph(trains)  # _____________________________________________________ Id всех городов
    data = form.cleaned_data  # ______________________________________________________ Данные, переданные пользователем
    user_from_city = data['from_city']  # ____________________________________________ Откуда (от пользователя)
    user_to_city = data['to_city']  # ________________________________________________ Куда (от пользователя)
    user_cities = data['cities']  # __________________________________________________ Через города (от пользователя)
    user_travel_time = data['route_form_travel_time']  # _____________________________ Время в пути (от пользователя)
    all_routes = list(dfs_paths(graph, user_from_city.id, user_to_city.id))  # _______ Список всех возможных маршрутов
    if not len(all_routes):  # _______________________________________________________ Если нет ни одного маршрута
        raise ValueError('Маршрута удовлетворяющего условиям поиска не существует')

    right_routes = get_through_cities(user_cities, all_routes)  # ____________________ Маршруты через заданные города
    routes = get_by_travel_time(trains, right_routes, user_travel_time)  # ___________ Маршруты по заданному времени
    sorted_routes = sort_by_travel_time(routes)  # ___________________________________ Сортированные маршруты по времени

    context['routes'] = sorted_routes
    context['cities'] = {
        'from_city': user_from_city,
        'to_city': user_to_city,
    }
    return context


def get_graph(trains) -> dict:
    """ Функция получения id всех городов, через которые проходят поезда.
    Итоговый словарь передается в функцию get_routes """

    graph = {}  # ____________________________________________________________________ Словарь {'Откуда': 'Куда'}
    for train in trains:
        graph.setdefault(train.from_city_id, set())  # _______________________________ Вершина
        graph[train.from_city_id].add(train.to_city_id)  # ___________________________ Значения
    return graph


def dfs_paths(graph, start, goal) -> list:
    """ Функция поиска всех возможных маршрутов из одного города в другой.
    Вариант посещения одного и того же города более одного раза, не рассматривается.
    Итоговый список передается в функцию get_routes """

    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_through_cities(user_cities, all_routes) -> list:
    """ Функция отбора маршрутов через заданные пользователем города.
    Итоговый список передается в функцию get_routes """

    if user_cities:  # ________________________________________ Если есть города, через которые нужно проехать
        user_cities_id = [city.id for city in user_cities]  # _ Список с id городов пользователя
        right_ways = []
        for route in all_routes:
            if all(city in route for city in user_cities_id):
                right_ways.append(route)  # ___________________ Добавляем маршрут, через выбранные пользователем города
        if not right_ways:
            if len(user_cities_id) == 1:
                raise ValueError('Нет маршрута через заданный город')
            else:
                raise ValueError('Нет маршрута через заданные города')
    else:  # __________________________________________________ Если не выбраны города, через которые нужно проехать
        right_ways = all_routes
    return right_ways


def get_by_travel_time(trains, right_routes, user_travel_time) -> list:
    """ Функция отбора маршрутов по заданному пользователем времени в пути.
    Итоговый список передается в функцию get_routes """

    routes = []
    all_trains = {}  # ______________________________________________________________ Словарь {id откуда,id куда: Поезд}
    for train in trains:
        all_trains.setdefault((train.from_city_id, train.to_city_id), [])
        all_trains[(train.from_city_id, train.to_city_id)].append(train)

    for route in right_routes:
        tmp_dct = {'trains': [], 'ids': []}  # ______________________________________ {Общее время в пути: поезда}
        total_time = 0  # ___________________________________________________________ Общее время в пути
        for index in range(len(route) - 1):  # ______________________________________ Проходимся по всем парам городов
            id_from, id_to = route[index], route[index + 1]
            tmp_train = all_trains[id_from, id_to][0]
            total_time += tmp_train.travel_time
            tmp_dct['ids'].append([id_from, id_to])
            tmp_dct['trains'].append(tmp_train)
        tmp_dct['total_time'] = total_time
        if total_time <= user_travel_time:  # _______________________________________ Если общее время в пути меньше
            routes.append(tmp_dct)  # _______________________________________________ заданного, то добавляем маршрут

    if not routes:  # _______________________________________________________________ Если список пуст, то нет маршрутов
        raise ValueError('Время в дороге больше выбранного Вами. Измените время.')  # удовлетворяющих заданные условия
    return routes


def sort_by_travel_time(routes) -> list:
    """ Функция сортировки маршрутов по времени в пути.
    Итоговый список передается в функцию get_routes """

    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = sorted(list(set(route['total_time'] for route in routes)))  # _______ Список неповторяющихся времен
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    return sorted_routes


def get_cleaned_form(data) -> object:
    """ Функция получения очищенных данных для формы.
    Итоговый объект передается в контроллер add_route_view """

    logic_trains_ids = get_trains_ids(data['ids'])
    from_city_id = int(data['from_city'])
    to_city_id = int(data['to_city'])
    total_time = int(data['total_time'])

    tmp_trains_ids = data['trains'].split(',')
    trains_ids = [int(_id) for _id in tmp_trains_ids if _id.isdigit()]

    trains = Train.objects.filter(id__in=trains_ids).select_related('from_city', 'to_city')
    cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()

    form = RouteModelForm(initial={
        'from_city': cities[from_city_id],
        'to_city': cities[to_city_id],
        'route_travel_time': total_time,
        'ids': logic_trains_ids,
        'trains': trains,
    })
    return form


def get_trains_ids(ids) -> list:
    """ Функция получения IDs поездов для выстраивания логической цепочки следования.
    Итоговый список передается в функцию get_cleaned_form """

    re_ids = findall('\d+', ids)  # _________________________________________________ Поиск всех индексов в строке
    trains_ids, index = [], 0
    while True:  # __________________________________________________________________ Цикл упаковки индексов
        pair = [int(re_ids[index]), int(re_ids[index + 1])]
        trains_ids.append(pair)
        if index == len(re_ids) - 2:
            break
        index += 2
    return trains_ids


def sort_trains(route, trains) -> list:
    """ Функция выстраивания логической цепочки следования поездов.
        Итоговый список передается в контроллер route_detail_view. """

    sorted_trains = []
    trains_ids = route.ids
    for index in range(len(trains)):
        for train in trains:
            pair = [train.from_city_id, train.to_city_id]
            if pair == trains_ids[index]:
                sorted_trains.append(train)
                break
    return sorted_trains
