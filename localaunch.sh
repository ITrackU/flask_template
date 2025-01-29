#!/bin/bash

# Créer un environnement virtuel
python3 -m venv myenv
if [ $? -ne 0 ]; then
    echo "Erreur lors de la création de l'environnement virtuel"
    exit 1
fi

# Activer l'environnement virtuel
source myenv/bin/activate  # Sous Windows, utilise "myenv\\Scripts\\activate"
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'activation de l'environnement virtuel"
    exit 1
fi

# Installer les dépendances
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'installation des dépendances"
    exit 1
fi

# Initialiser la base de données
python init_db.py
# Lancer l'application Flask
python app.py
if [ $? -ne 0 ]; then
    echo "Erreur lors du lancement de l'application Flask"
    exit 1
fi

# Désactiver l'environnement virtuel
deactivate
