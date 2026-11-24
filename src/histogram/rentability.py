import pandas as pd
import plotly.express as px
import streamlit as st

from config import Config

potions = pd.read_excel(Config.DataFileSource, sheet_name="potions")
potions_inventeurs = pd.read_excel(
    Config.DataFileSource, sheet_name="potions-inventeurs"
)
diluant_price = pd.read_excel(Config.DataFileSource, sheet_name="prix-diluants")
ingredients_price = pd.read_excel(Config.DataFileSource, sheet_name="liste-ingredients")


# Fait la conversion d'un souffle vers une pincée
def breath_to_pinch(quantity):
    return quantity * 0.7


# Fait la conversion d'un nuage vers une pincée
def cloud_to_pinch(quantity):
    return breath_to_pinch(quantity * 5)


# Fait la conversion d'une poignée vers une pincée
def handle_to_pinch(quantity):
    return cloud_to_pinch(quantity * 3)


# Fait la conversion d'une once vers une pincée
def ounce_to_pinch(quantity):
    return handle_to_pinch(quantity * 2)


# Converti chaque unité des potions en pincée
for potion in potions.values:
    for ingredient in range(1, 12, 4):
        if not (pd.isna(potion[ingredient])):
            if potion[ingredient + 2] != "Pincée":
                if potion[ingredient + 2] == "Souffle":
                    potion[ingredient + 1] = breath_to_pinch(potion[ingredient + 1])
                elif potion[ingredient + 2] == "Nuage":
                    potion[ingredient + 1] = cloud_to_pinch(potion[ingredient + 1])
                elif potion[ingredient + 2] == "Poignée":
                    potion[ingredient + 1] = handle_to_pinch(potion[ingredient + 1])
                elif potion[ingredient + 2] == "Once":
                    potion[ingredient + 1] = ounce_to_pinch(potion[ingredient + 1])


# Récupère le coût d'un ingrédient passé en paramètre
def get_ingredient_cost(ingredient):
    price = ingredients_price.loc[
        ingredients_price["ingredients"] == ingredient.strip(), "prix"
    ].values[0]
    return price


# Récupère le coût d'un diluant passé en paramètre
def get_diluant_cost(diluant):
    price = diluant_price.loc[
        diluant_price["diluant"] == diluant.strip(), "prix"
    ].values[0]
    return price


# Calcule le coût de production d'une potion
def calculate_potion_cost(potion):
    price = 0
    for ingredient in range(1, 12, 4):
        if not (pd.isna(potion[ingredient])):
            price += get_ingredient_cost(potion[ingredient])
    price += get_diluant_cost(potion[17])
    return price


# Calcule la rentabilité d'une potion passée en paramètre
def calculate_potion_rentability(potion):
    cost = calculate_potion_cost(potion)
    rentability = potion[18] - cost
    return rentability


def display_histogram():
    rentability_data = []

    for potion in potions.values:
        rentability = calculate_potion_rentability(potion)

        rentability_data.append(
            {
                "potion": potion[0],
                "Rentabilité": rentability,
                "type-magie-potion": potions_inventeurs.loc[
                    potions_inventeurs["potion"] == potion[0], "type-magie-potion"
                ].iloc[0],
            }
        )

    rentability_df = pd.DataFrame(rentability_data)
    rentability_df = rentability_df.sort_values(by="Rentabilité")

    top_10 = rentability_df.nlargest(10, "Rentabilité").sort_values(
        "Rentabilité", ascending=False
    )

    fig = px.bar(
        top_10,
        x="Rentabilité",
        y="potion",
        orientation="h",
        color="type-magie-potion",
        color_discrete_map={
            "Bleue": "#2563eb",
            "Blanche": "#f8fafc",
            "Noire": "#252525",
            "Rouge": "#dc2626",
            "Verte": "#16a34a",
            "Pourpre": "#9333ea",
        },
        category_orders={"potion": top_10["potion"].tolist()},
        title="Les 10 potions les plus rentables",
    )

    fig.update_yaxes(
        tickmode="array",
        tickvals=top_10["potion"].tolist(),
        ticktext=top_10["potion"].tolist(),
    )

    fig.update_layout(height=600, margin=dict(l=300, r=50, t=80, b=50))

    st.plotly_chart(fig, use_container_width=True)
