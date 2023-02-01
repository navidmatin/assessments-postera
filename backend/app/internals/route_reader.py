import json
import aiofiles

from app.internals.models.route import Route
from app.internals.view_models.d3_tree_molecule_node import D3TreeMoleculeNode


class RouteReader:
    async def load_routes():
        routes = []
        # can use libraries to read the file async
        async with aiofiles.open("app/internals/routes.json", mode="r") as file:
            content = await file.read()

        parsed_routes = json.loads(content)
        for route_info in parsed_routes:
            routes.append(Route().parse_route_info(route_info))

        return routes

    def create_d3_tree_from_route(route: Route):
        resulting_molecule = route.get_resulting_molecule()
        return D3TreeMoleculeNode(resulting_molecule, route)
