from typing import List

from app.internals.models.molecule import Molecule
from app.internals.models.route import Route


class D3TreeMoleculeNode:
    def __init__(self, molecule: Molecule, route: Route):
        self.name = None
        self.children = []
        self.attributes = dict()
        self.__convert_molecule_to_attributes(molecule)
        self.__convert_reactions_to_children(molecule, route)

    def __convert_molecule_to_attributes(self, molecule: Molecule):
        self.name = molecule.smiles
        # self.attributes["acquisition_catalogs"] = molecule.acquisition_catalogs

    def __convert_reactions_to_children(self, molecule: Molecule, route: Route) -> None:
        base_molecules = route.get_base_molecules_from_reaction(
            molecule.smiles)
        for base_molecule in base_molecules:
            self.children.append(D3TreeMoleculeNode(base_molecule, route))
