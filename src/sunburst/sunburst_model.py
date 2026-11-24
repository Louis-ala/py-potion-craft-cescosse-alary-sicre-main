class Potion:
    name: str
    creator: str
    magic_type: str

    def __init__(self, name: str, magic_type: str) -> None:
        self.name = name
        self.magic_type = magic_type


class Skill:
    name: str
    magic_type: str

    def __init__(self, name: str, magic_type: str) -> None:
        self.name = name
        self.magic_type = magic_type
        self.potions: list[Potion] = []

    def add_potion(self, potion: Potion) -> None:
        self.potions.append(potion)


class MagicType:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self.skills: list[Skill] = []
        self.potions: list[Potion] = []

    def add_skill(self, skill: Skill) -> None:
        self.skills.append(skill)

    def add_potion(self, potion: Potion) -> None:
        self.potions.append(potion)
