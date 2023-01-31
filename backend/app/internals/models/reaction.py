from typing import List


class Reaction:
    def __init__(self, name: str, target: str, sources: List[str]):
        self.name = name
        self.target = target
        self.sources = sources

    def __hash__(self):
        return hash((self.name, self.target, ' '.join(self.sources)))

    def __eq__(self, other: object) -> bool:
        return (self.name, self.target, ' '.join(self.sources)) == (other.name, other.target, ' '.join(other.sources))

    def __ne__(self, other: object) -> bool:
        return not (self == other)
