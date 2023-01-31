class Catalog:
    def __init__(self, molecule_smiles, vendor_id, name, lead_time_weeks):
        self.vendor_id = vendor_id
        self.name = name
        self.molecule_smiles = molecule_smiles
        self.lead_time_weeks = lead_time_weeks

    def __hash__(self):
        return hash((self.name, self.vendor_id, self.molecule_smiles))

    def __eq__(self, other: object) -> bool:
        return (self.name, self.vendor_id, self.molecule_smiles) == (other.name, other.vendor_id, other.molecule_smiles)

    def __ne__(self, other: object) -> bool:
        return not (self == other)
