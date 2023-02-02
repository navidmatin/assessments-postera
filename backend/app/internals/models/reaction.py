from typing import List


class Reaction:
    # TODO: In case of production we should handle scenarios that a reaction can have multiple targets, right now the same reaction would be repeated twice for different target
    def __init__(self, name: str, target: str, sources: List[str], route_id: str = None):
        self.name = name
        self.target = target
        self.sources = sources
        self.route_id = route_id
        # Added for multi route reactions
        self.id = f'{self.name}-{self.target}'

    def __hash__(self):
        return hash((self.name, self.target, ' '.join(self.sources), self.route_id))

    def __eq__(self, other: object) -> bool:
        return (self.name, self.target, ' '.join(self.sources), self.route_id) == (other.name, other.target, ' '.join(other.sources), self.route_id)

    def __ne__(self, other: object) -> bool:
        return not (self == other)
