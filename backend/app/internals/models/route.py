from typing import List
from app.internals.models.catalog import Catalog
from app.internals.models.molecule import Molecule
from app.internals.models.reaction import Reaction


class Route:
    def __init__(self) -> None:
        self.score = None
        self.resulting_molecule = None
        self.smiles_to_molecules = dict()

    def parse_route_info(self, route_info):
        reactions = route_info['reactions']
        molecules = route_info['molecule']
        self.score = route_info['score']

        smiles_to_molecules = self.smiles_to_molecules
        non_building_block_smiles = set()
        reaction_source_smiles = set()

        for molecule in molecules:
            catalog_set = set()
            smiles = molecule['smiles']
            for catalog_entry in molecule['catalog_entries']:
                catalog_set.add(
                    Catalog(
                        smiles,
                        catalog_entry['vendor_id'],
                        catalog_entry['catalog_name'],
                        catalog_entry['lead_time_weeks'])
                )
            smiles_to_molecules[smiles] = Molecule(
                smiles=smiles, is_building_block=molecule['is_building_block'], acquisition_catalogs=catalog_set)
            if not molecule['is_building_block']:
                non_building_block_smiles.add(smiles)

        for reaction in reactions:
            reaction_target = reaction['target']
            reaction = Reaction(
                reaction['name'], reaction_target, reaction['sources'])
            # Let's add source smiles to a set so we can check them later easily
            reaction_source_smiles = reaction_source_smiles.union(
                reaction['sources'])
            if not reaction_target in smiles_to_molecules:
                smiles_to_molecules[reaction_target] = Molecule(
                    reaction_target)

            smiles_to_molecules[reaction_target].creation_reactions.add(
                reaction)

        # Figure out the top level resulting molecule
        for target in non_building_block_smiles.keys:
            if not target in reaction_source_smiles:
                self.resulting_molecule = target
                break

    def molecule(self, smiles) -> Molecule:
        if smiles in self.smiles_to_molecules:
            return self.smiles_to_molecules[smiles]

        return None

    def get_base_molecules(self, smiles) -> List[Molecule]:
        if not smiles in self.smiles_to_molecules:
            return None

        base_molecules = []
        molecule = self.smiles_to_molecules[smiles]
        for reaction in molecule.creation_reactions:
            for source in reaction.sources:
                base_molecules.append(self.smiles_to_molecules[source])

        return base_molecules
