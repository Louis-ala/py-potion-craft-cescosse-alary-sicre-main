import re

import pandas as pd
import streamlit as st

from config import Config


def name_key(name):
    return re.sub(r"[\W_]", "", name).lower()


# Fonction pour charger les données et nettoyer les noms d'inventeurs.
def load_potions_inventors():
    potions_inventor = pd.read_excel(
        Config.DataFileSource, sheet_name="potions-inventeurs"
    )
    list_inventors = pd.read_excel(Config.DataFileSource, sheet_name="liste-inventeurs")

    reference_by_key = {
        name_key(pseudo + " " + lignee): (pseudo, lignee)
        for pseudo, lignee in zip(list_inventors["pseudo"], list_inventors["lignee"])
    }

    def split_inventor_name(name):
        if pd.isna(name):
            return ("Inconnus", "Inconnus")
        # Nom introuvable dans la liste : on le garde en entier dans le pseudo
        return reference_by_key.get(name_key(name), (name, ""))

    # Remplace la colonne "inventeur" par deux colonnes "pseudo" et "lignee"
    split_names = potions_inventor["inventeur"].apply(split_inventor_name)
    potions_inventor["pseudo"] = [pseudo for pseudo, lignee in split_names]
    potions_inventor["lignee"] = [lignee for pseudo, lignee in split_names]
    potions_inventor = potions_inventor.drop(columns="inventeur")
    return potions_inventor


potions_inventor = load_potions_inventors()


# Tableau des lignées : une ligne par lignée, avec sa couleur

# Une couleur par lignée
colors = [
    "#e6194b",
    "#3cb44b",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#42d4f4",
    "#f032e6",
    "#9a6324",
]

# Lignées différentes
lignee_names = sorted(
    lignee
    for lignee in potions_inventor["lignee"].unique()
    if lignee not in ("", "Inconnus")
)

# "Ajout inconnus au tableau"
Descendance = pd.DataFrame(
    {
        "lignee": lignee_names + ["Inconnus"],
        "couleur": colors[: len(lignee_names)] + ["#808080"],
    }
)
