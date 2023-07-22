from trains.models import Train


def dfs_paths(graph, start, goal):
    """
    Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города более одного раза,
    не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(query_set):
    graph = {}
    for query in query_set:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    query_set = Train.objects.all()
    graph = get_graph(query_set)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travel_time = data['route_form_travel_time']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_ways):
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')
    # Отбор маршрутов через заданные пользователем города. ___________________
    if cities:
        temp_cities = [city.id for city in cities]
        right_ways = []
        for way in all_ways:
            if all(city in way for city in temp_cities):
                right_ways.append(way)
        if not right_ways:
            raise ValueError('Маршрут через эти города невозможен')
    else:
        right_ways = all_ways
    # Отбор маршрутов по заданному пользователем времени в пути. _____________
    routes = []
    all_trains = {}
    for query in query_set:
        all_trains.setdefault((query.from_city_id, query.to_city_id), [])
        all_trains[(query.from_city_id, query.to_city_id)].append(query)
    for way in right_ways:
        temp = {'trains': []}
        total_time = 0
        for index in range(len(way) - 1):
            query_set = all_trains[(way[index], way[index + 1])]
            query = query_set[0]
            total_time += query.travel_time
            temp['trains'].append(query)
        temp['total_time'] = total_time
        if total_time <= travel_time:
            routes.append(temp)
    if not routes:
        raise ValueError('Время в пути больше заданного')
    # Сортировка маршрутов по времени в пути. ________________________________
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(route['total_time'] for route in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {
        'from_city': from_city.name,
        'to_city': to_city.name,
    }
    return context
