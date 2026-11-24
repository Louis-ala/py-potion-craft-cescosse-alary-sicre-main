import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from sunburst.sunburst_utilities import (
    get_all_potions,
    get_all_skills_and_magictypes,
    link_potions_to_skills,
)


def display_sunburst():
    st.title("Hiérarchie des Potions")

    potions = get_all_potions()
    skills, magictypes = get_all_skills_and_magictypes()
    link_potions_to_skills(potions, magictypes)

    nb_potions = sum(len(magic.potions) for magic in magictypes)

    root_label = f"{nb_potions}<br>potions"  # Rond principal du sunburst

    data = []
    for magic in magictypes:
        m_name = magic.name
        m_skills = magic.skills
        m_potions = magic.potions

        # Affichage selectif des données permet d'afficher si un magictype est vide ou si il contient des compétences ou des potions
        if not m_skills and not m_potions:
            data.append(
                {"Root": root_label, "Magic": m_name, "Skill": None, "Potion": None}
            )
        elif m_skills and not m_potions:
            for skill in m_skills:
                data.append(
                    {
                        "Root": root_label,
                        "Magic": m_name,
                        "Skill": skill.name,
                        "Potion": None,
                    }
                )
        elif not m_skills and m_potions:
            for potion in m_potions:
                data.append(
                    {
                        "Root": root_label,
                        "Magic": m_name,
                        "Skill": "\u200b",
                        "Potion": potion.name,
                    }
                )
        else:
            nb_skills = len(m_skills)
            for i, potion in enumerate(m_potions):
                skill_name = m_skills[i % nb_skills].name
                data.append(
                    {
                        "Root": root_label,
                        "Magic": m_name,
                        "Skill": skill_name,
                        "Potion": potion.name,
                    }
                )

    df = pd.DataFrame(data)

    color_mapping = {
        "Noire": "#5C6670",
        "Bleue": "#4B9CE3",
        "Rouge": "#E85D67",
        "Verte": "#36B37E",
        "Blanche": "#E2E6E9",
        "Pourpre": "#B07CE8",
        "(?)": "#111111",  # Couleur par defaut de plotly
    }

    fig = px.sunburst(
        df,
        path=["Root", "Magic", "Skill", "Potion"],
        color="Magic",
        color_discrete_map=color_mapping,
    )

    fig.update_traces(
        textinfo="text",
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b>",
        marker=dict(line=dict(color="#111111", width=2)),
        leaf=dict(opacity=1),
    )

    potions_name = df["Potion"].dropna().unique()
    text_to_display = [
        "" if label in potions_name else label for label in fig.data[0].labels
    ]
    fig.update_traces(text=text_to_display)

    for magic in magictypes:
        color = color_mapping.get(magic.name, "#FFFFFF")
        n_pot = len(magic.potions)
        n_ski = len(magic.skills)

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=14, color=color, symbol="square"),
                name=f"{n_pot} potions • {n_ski} compétences",
                legendgroup=magic.name,
                legendgrouptitle=dict(
                    text=magic.name, font=dict(size=16, color="white")
                ),
                showlegend=True,
                hoverinfo="none",
            )
        )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(t=20, l=0, r=150, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        uniformtext=dict(minsize=11, mode="hide"),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=13, color="#9CA3AF"),
            itemclick=False,
            itemdoubleclick=False,
            tracegroupgap=10,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
