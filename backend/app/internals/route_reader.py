import json

from backend.app.internals.models.route import Route


class RouteReader:
    def load_routes():
        # can use libraries to read the file async
        routes_json = open("routes.json", "r")
        routes = []
        parsed_routes = json.loads(routes_json)
        for route_info in parsed_routes:
            routes.append(Route().parse_route_info(route_info))

        return routes
