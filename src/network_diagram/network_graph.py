import networkx as nx
import plotly.graph_objects as go
import streamlit as st

# Import le tableau des inventeurs avec leur potions liée.
from network_diagram.network_data import Descendance, potions_inventor

color_by_lignee = dict(zip(Descendance["lignee"], Descendance["couleur"]))


# Nom affiché pour chaque inventeur
def inventor_label(pseudo, lignee):
    if pseudo == lignee:
        return pseudo
    return pseudo + " " + lignee


# --- Création du graphe ---
def display_network_graph():
    graph = nx.Graph()
    for potion, pseudo, lignee in zip(
        potions_inventor["potion"],
        potions_inventor["pseudo"],
        potions_inventor["lignee"],
    ):
        inventor = inventor_label(pseudo, lignee)
        color = color_by_lignee.get(lignee, "#cccccc")
        graph.add_node(inventor, kind="inventeur", color=color, lignee=lignee)
        graph.add_node(potion, kind="potion", color=color, lignee=lignee)
        graph.add_edge(inventor, potion, weight=0.2)

    inventors = [n for n, data in graph.nodes(data=True) if data["kind"] == "inventeur"]
    potions = [n for n, data in graph.nodes(data=True) if data["kind"] == "potion"]

    # NetworkX calcule la position des noeuds : chaque inventeur attire ses potions autour de lui
    positions = nx.spring_layout(graph, k=0.7, iterations=300, seed=6)

    # --- Dessin avec Plotly ---
    figure = go.Figure()

    # Liens
    edge_x, edge_y = [], []
    for source, target in graph.edges:
        edge_x += [positions[source][0], positions[target][0], None]
        edge_y += [positions[source][1], positions[target][1], None]
    figure.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            hoverinfo="skip",
            line=dict(color="lightgray", width=1),
            showlegend=False,
        )
    )

    # Potions
    for lignee, color in color_by_lignee.items():
        nodes = [n for n in potions if graph.nodes[n]["lignee"] == lignee]
        figure.add_trace(
            go.Scatter(
                x=[positions[n][0] for n in nodes],
                y=[positions[n][1] for n in nodes],
                mode="markers+text",
                text=nodes,
                textposition="bottom center",
                textfont=dict(size=8, color="black"),
                marker=dict(size=10, color=color, line=dict(color="black", width=1)),
                name=lignee,
                legendgroup=lignee,
                hovertemplate="%{text}<extra>" + lignee + "</extra>",
            )
        )

    # Inventeurs
    for lignee, color in color_by_lignee.items():
        nodes = [n for n in inventors if graph.nodes[n]["lignee"] == lignee]
        # Nombre de potions de chaque inventeur
        potion_counts = [graph.degree(n) for n in nodes]
        figure.add_trace(
            go.Scatter(
                x=[positions[n][0] for n in nodes],
                y=[positions[n][1] for n in nodes],
                mode="markers+text",
                text=nodes,
                textposition="middle center",
                textfont=dict(size=11, color="black", weight="bold"),
                # Plus un inventeur a de potions, plus sa bulle est grosse
                marker=dict(
                    size=[4 + 8 * count for count in potion_counts],
                    color=color,
                    line=dict(color="black", width=1),
                ),
                name=lignee,
                legendgroup=lignee,
                showlegend=False,
                hovertemplate="%{text}<extra>" + lignee + "</extra>",
            )
        )

    figure.update_layout(
        title="Inventeurs et leurs potions, par lignée",
        legend_title_text="Lignée",
        height=900,
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    # --- Page Streamlit ---
    st.title("Diagramme réseau des inventeurs")
    st.plotly_chart(figure, width="stretch")
