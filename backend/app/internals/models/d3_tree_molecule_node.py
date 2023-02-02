from typing import List

from app.internals.models.molecule import Molecule
from app.internals.models.route import Route


class D3TreeMoleculeNode:
    def __init__(self, molecule: Molecule, route: Route, smiles_to_routes: dict() = None, reactions_to_all_routes: dict() = None):
        self.name = molecule.smiles
        self.children = []
        self.attributes = dict()
        self.__convert_molecule_to_attributes(
            molecule, smiles_to_routes)
        self.__convert_reactions_to_children(
            molecule, route, reactions_to_all_routes=reactions_to_all_routes, smiles_to_routes=smiles_to_routes)

    def __convert_molecule_to_attributes(self, molecule: Molecule, smiles_to_routes=None):
        self.attributes["acquisition_catalogs"] = molecule.acquisition_catalogs
        self.attributes["route_id"] = molecule.route_id
        self.attributes["all_route_ids"] = smiles_to_routes and smiles_to_routes.get(
            self.name)

    def __convert_reactions_to_children(self, molecule: Molecule, route: Route, smiles_to_routes=None, reactions_to_all_routes=None) -> None:
        base_molecules = route.get_base_molecules_from_reaction(
            molecule.smiles)
        for base_molecule in base_molecules:
            self.children.append(D3TreeMoleculeNode(
                base_molecule, route, smiles_to_routes=smiles_to_routes, reactions_to_all_routes=reactions_to_all_routes))

        self.attributes["reactions"] = []
        for reaction in molecule.creation_reactions:
            self.attributes["reactions"].append(reaction.name)
            self.attributes["reaction_in_other_routes"] = {
                'reaction_id': reaction.id, 'other_route_ids': reactions_to_all_routes and reactions_to_all_routes.get(reaction.id)}
