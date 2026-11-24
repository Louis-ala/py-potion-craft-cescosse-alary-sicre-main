import pandas as pd

from config import Config

# Tri des compétences par nombre de potions


def get_competences_count():

    magic_types = pd.read_excel(
        Config.DataFileSource, sheet_name="liste-types-de-magie"
    )
    potions_inventor = pd.read_excel(
        Config.DataFileSource, sheet_name="potions-inventeurs"
    )

    nb_color = potions_inventor["type-magie-potion"].value_counts()

    competences_count = []

    for index, row in magic_types.iterrows():
        couleur = row["type_de_magie"]
        nb_potions = int(
            nb_color.get(couleur, 0)
        )  #  nombre de potions de ce type de magie

        for competence in row["competences"].split(";"):
            # vérifie si la compétence est déjà dans le tableau
            trouvee = False
            for ligne in competences_count:
                if ligne[0] == competence:
                    ligne[1] += nb_potions  # oui : on ajoute au total existant
                    trouvee = True
                    break

            if not trouvee:
                competences_count.append(
                    [competence, nb_potions]
                )  # non : nouvelle ligne

    return competences_count
