### py-potion-craft-cescosse-alary-sicre

## Installation du projet :

- Cloner le dépôt :
```bash
git clone https://github.com/ilian-458/py-potion-craft-cescosse-alary-sicre.git
```

- Créer un environnement virtuel :
```bash
python -m venv .venv
```

- Activer l'environnement virtuel :
(linux)
```bash
source .venv/bin/activate
```
(windows)
```bash
.venv\Scripts\activate
```

- Installer les dépendances :
```bash
pip install -r requirements.txt
```

- Lancer le projet :
```bash
streamlit run src/main.py
```

# Ajout de données

Nous avons ajouté au fichier potions-craft.xlsx des données sur la feuille liste-ingredient pour avoir dans la liste des ingrédients tous les ingrédients utilisés dans les potions car certains étaient manquants.

# Diagramme Sunburst

Nous avons trouvé un soucis avec les données, il est impossible d'après les données du tableur d'identifier qu'elle compétence est en lien avec une potion, nous avons donc divisé en part égale toutes les potions d'un même type de magie par le nombre de compétences.

L'architecture de ce diagramme est la suivante:
- Un modèle de données pour visualiser les données et les relations
- Un service qui contient des méthodes pour instancier et trier les données dans les modèles de données
- Une interface utilisateur (le diagramme) qui utilise les données

# Diagramme de Kiviat

L'architecture de ce diagramme est la suivante:
- Un service qui contient des méthodes afin d'etraire le données du tableur et de les trier
- Une interface utilisateur (le diagramme) qui utilise les données pour formér le diagramme de Kiviat

# Diagramme de réseau

L'architecture de ce diagramme est la suivante:
- Un service qui contient des méthodes afin d'etraire le données du tableur et de les trier
- Une interface utilisateur (le diagramme) qui utilise les données pour formér le diagramme de réseau
