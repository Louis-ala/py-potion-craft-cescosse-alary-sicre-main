import pandas as pd
from pandas import DataFrame

from config import Config
from sunburst.sunburst_model import MagicType, Potion, Skill


def get_all_potions() -> list[Potion]:

    potions_excel_list: DataFrame = pd.read_excel(
        Config.DataFileSource, "potions-inventeurs"
    )

    potion_list: list[Potion] = []

    for _, potion in potions_excel_list.iterrows():
        potion_obj = Potion(
            name=potion["potion"],
            magic_type=potion["type-magie-potion"],
        )
        potion_list.append(potion_obj)

    return potion_list


def get_all_skills_and_magictypes() -> tuple[list[Skill], list[MagicType]]:
    skills_magic_link_list: DataFrame = pd.read_excel(
        Config.DataFileSource, "liste-types-de-magie"
    )

    skill_dict: dict[str, Skill] = {}
    magictype_list: list[MagicType] = []

    for _, row in skills_magic_link_list.iterrows():
        magic_name: str = row["type_de_magie"]
        magic_obj = MagicType(name=magic_name)
        magictype_list.append(magic_obj)

        raw_skills = row["competences"]

        if pd.notna(raw_skills):
            skill_names = str(raw_skills).split(";")

            for skill_name in skill_names:
                clean_skill_name = skill_name.strip()
                if not clean_skill_name:
                    continue

                if clean_skill_name not in skill_dict:
                    skill_dict[clean_skill_name] = Skill(
                        name=clean_skill_name, magic_type=magic_name
                    )

                skill_obj = skill_dict[clean_skill_name]
                magic_obj.add_skill(skill_obj)

    return list(skill_dict.values()), magictype_list


def link_potions_to_skills(
    potion_list: list[Potion], magictype_list: list[MagicType]
) -> None:
    magic_dict = {magic.name: magic for magic in magictype_list}

    for potion in potion_list:
        magic_name = potion.magic_type

        if magic_name in magic_dict:
            magic_obj = magic_dict[magic_name]

            magic_obj.add_potion(potion)

            for skill in magic_obj.skills:
                skill.add_potion(potion)
