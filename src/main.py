import streamlit as st

from histogram.rentability import display_histogram
from kiviat_chart.kiviat_chart import display_kiviat
from network_diagram.network_graph import display_network_graph
from sunburst.sunburst_ihm import display_sunburst

if "actual_page" not in st.session_state:
    st.session_state.actual_page = "accueil"


def changer_page(nom_de_page):
    st.session_state.actual_page = nom_de_page


if st.session_state.actual_page == "accueil":
    st.title("Tableau de bord des Potions")
    st.write(
        "Bienvenue ! Cliquez sur un bouton pour afficher le schéma correspondant :"
    )

    st.button(
        "Afficher le histogramme des rentabilités",
        on_click=changer_page,
        args=("histogram",),
    )
    st.button(
        "Afficher un diagramme de tri des compétences et type de magie (sunburst)",
        on_click=changer_page,
        args=("sunburst",),
    )
    st.button(
        "Afficher le nombre de potions par compétence (kiviat)",
        on_click=changer_page,
        args=("kiviat",),
    )
    st.button(
        "Afficher le diagramme réseau des inventeurs",
        on_click=changer_page,
        args=("network",),
    )

elif st.session_state.actual_page == "sunburst":
    st.button("Retour à l'accueil", on_click=changer_page, args=("accueil",))
    st.divider()
    display_sunburst()

elif st.session_state.actual_page == "kiviat":
    st.button("Retour à l'accueil", on_click=changer_page, args=("accueil",))
    st.divider()
    display_kiviat()

elif st.session_state.actual_page == "histogram":
    st.button("Retour à l'accueil", on_click=changer_page, args=("accueil",))
    st.divider()
    display_histogram()

elif st.session_state.actual_page == "network":
    st.button("Retour à l'accueil", on_click=changer_page, args=("accueil",))
    st.divider()
    display_network_graph()
