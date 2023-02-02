import json
import aiofiles
from typing import List

from app.internals.models.route import Route
from app.internals.models.d3_tree_molecule_node import D3TreeMoleculeNode
import pdb


class RouteHelper:
    async def load_routes() -> List[Route]:
        routes = []
        # can use libraries to read the file async
        async with aiofiles.open("routes.json", mode="r") as file:
            content = await file.read()

        parsed_routes = json.loads(content)
        for index, route_info in enumerate(parsed_routes):
            # pdb.set_trace()
            routes.append(Route().parse_route_info(route_info, id=index))

        return routes

    def analyze_routes_for_overlaps(routes: List[Route]):

        map_of_smiles_to_route_ids = dict()
        map_of_reactions_to_route_ids = dict()
        for route in routes:
            for molecule in route.smiles_to_molecules.values():
                if not molecule.smiles in map_of_smiles_to_route_ids:
                    map_of_smiles_to_route_ids[molecule.smiles] = set()
                map_of_smiles_to_route_ids[molecule.smiles].add(
                    molecule.route_id)

                # handle reactions
                for reaction in molecule.creation_reactions:
                    if not reaction.id in map_of_reactions_to_route_ids:
                        map_of_reactions_to_route_ids[reaction.id] = set()
                    map_of_reactions_to_route_ids[reaction.id].add(
                        reaction.route_id)

        return {'smiles_to_routes': map_of_smiles_to_route_ids, 'reactions_to_routes': map_of_reactions_to_route_ids}

    def create_d3_tree_from_route(route: Route, route_analytics_result=None):
        resulting_molecule = route.get_resulting_molecule()
        return D3TreeMoleculeNode(resulting_molecule, route, route_analytics_result['smiles_to_routes'], route_analytics_result['reactions_to_routes'])
