from trains.models import Train


def get_routes(form) -> dict:
    """ Функция получения всех возможных маршрутов """
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
    (setdefault - чтобы не проверять есть ли ключ в графе) """
    graph = {}  # ____________________________________________________________________ Словарь {'Откуда': 'Куда'}
    for train in trains:
        graph.setdefault(train.from_city_id, set())      # ___________________________ Вершина
        graph[train.from_city_id].add(train.to_city_id)  # ___________________________ Значения
    return graph


def dfs_paths(graph, start, goal):
    """ Функция поиска всех возможных маршрутов из одного города в другой.
    Вариант посещения одного и того же города более одного раза, не рассматривается. """
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
    """ Функция отбора маршрутов через заданные пользователем города. """
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


def get_by_travel_time(trains, right_ways, user_travel_time) -> list:
    """ Функция отбора маршрутов по заданному пользователем времени в пути. """
    routes = []
    all_trains = {}  # ______________________________________________________________ Словарь {id откуда,id куда: Поезд}
    for train in trains:
        all_trains.setdefault((train.from_city_id, train.to_city_id), [])
        all_trains[(train.from_city_id, train.to_city_id)].append(train)

    for way in right_ways:
        tmp_dct = {'trains': []}  # _________________________________________________ {Общее время в пути: поезда}
        total_time = 0  # ___________________________________________________________ Общее время в пути
        for index in range(len(way) - 1):  # ________________________________________ Проходимся по всем парам городов
            tmp_train = all_trains[(way[index], way[index + 1])][0]
            total_time += tmp_train.travel_time
            tmp_dct['trains'].append(tmp_train)
        tmp_dct['total_time'] = total_time
        if total_time <= user_travel_time:  # _______________________________________ Если общее время в пути меньше
            routes.append(tmp_dct)  # _______________________________________________ заданного, то добавляем маршрут

    if not routes:  # _______________________________________________________________ Если список пуст, то нет маршрутов
        raise ValueError('Время в дороге больше выбранного Вами. Измените время.')  # удовлетворяющих заданные условия
    return routes


def sort_by_travel_time(routes) -> list:
    """ Функция сортировки маршрутов по времени в пути. """
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = sorted(list(set(route['total_time'] for route in routes)))  # _ Список неповторяющихся времен
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    return sorted_routes
