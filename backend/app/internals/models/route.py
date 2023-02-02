from typing import List
from app.internals.models.catalog import Catalog
from app.internals.models.molecule import Molecule
from app.internals.models.reaction import Reaction


class Route:
    def __init__(self) -> None:
        self.score = None
        self.resulting_molecule_smile = None
        self.smiles_to_molecules = dict()
        self.id = None

    def parse_route_info(self, route_info) -> 'Route':
        reactions = route_info['reactions']
        molecules = route_info['molecules']
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
                smiles=smiles, acquisition_catalogs=catalog_set)
            if not molecule['is_building_block']:
                non_building_block_smiles.add(smiles)

        for reaction in reactions:
            reaction_target = reaction['target']
            reaction_obj = Reaction(
                reaction['name'], reaction_target, reaction['sources'])
            # Let's add source smiles to a set so we can check them later easily
            reaction_source_smiles = reaction_source_smiles.union(
                reaction_obj.sources)
            if not reaction_target in smiles_to_molecules:
                smiles_to_molecules[reaction_target] = Molecule(
                    reaction_target)

            smiles_to_molecules[reaction_target].creation_reactions.add(
                reaction_obj)

        # Figure out the top level resulting molecule
        for target in non_building_block_smiles:
            if not target in reaction_source_smiles:
                self.resulting_molecule_smile = target
                break
        return self

    def get_resulting_molecule(self) -> Molecule:
        if not self.resulting_molecule_smile in self.smiles_to_molecules:
            return None

        return self.smiles_to_molecules[self.resulting_molecule_smile]

    def get_base_molecules_from_reaction(self, smiles) -> List[Molecule]:
        if not smiles in self.smiles_to_molecules:
            return None

        base_molecules = []
        molecule = self.smiles_to_molecules[smiles]
        for reaction in molecule.creation_reactions:
            for source in reaction.sources:
                base_molecules.append(self.smiles_to_molecules[source])

        return base_molecules
