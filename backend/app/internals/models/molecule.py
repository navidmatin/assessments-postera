from app.internals.models.reaction import Reaction
from app.internals.models.catalog import Catalog
from typing import Set
from typing import List


class Molecule:
    def __init__(self, smiles, creation_reactions: Set[Reaction] = None, acquisition_catalogs: Set[Catalog] = None):
        self.smiles = smiles
        self.creation_reactions = creation_reactions or set()
        self.acquisition_catalogs = acquisition_catalogs or set()
