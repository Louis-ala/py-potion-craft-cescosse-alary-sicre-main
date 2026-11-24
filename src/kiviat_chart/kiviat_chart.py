import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from kiviat_chart.excel_data import get_competences_count


def display_kiviat():

    competences_count = get_competences_count()

    # Création du graphique

    etiquettes = [
        f"{competence} <span style='color:{'#3DDC84'}'>{nombre}</span>"
        for competence, nombre in competences_count
    ]

    st.title("Compétences des potions")

    valeurs = [ligne[1] for ligne in competences_count]

    fig = go.Figure(
        go.Scatterpolar(
            r=valeurs + valeurs[:1],
            theta=etiquettes + etiquettes[:1],
            fill="toself",
            fillcolor="rgba(61, 220, 132, 0.18)",  # vert transparent
            line=dict(color="#3DDC84", width=3),
            marker=dict(color="#3DDC84", size=9),
            mode="lines+markers",  # points sur les sommets
            hovertemplate="%{theta}<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="#0B1117",
        showlegend=False,
        margin=dict(l=90, r=90, t=50, b=50),
        polar=dict(
            bgcolor="#0B1117",
            gridshape="linear",
            radialaxis=dict(
                range=[0, max(valeurs)],
                showticklabels=False,
                ticks="",
                showline=False,
                gridcolor="#232B36",
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
                gridcolor="#232B36",
                linecolor="#232B36",
                ticks="",
            ),
        ),
    )

    st.plotly_chart(fig)
