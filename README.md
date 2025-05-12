# G-nie-logiciel
---

# Projet Génie Logiciel - Gestion d'agenda

Ce projet contient une application client-serveur développée en Python.
Il utilise une interface graphique avec PyQt6 et communique via des sockets. Les données sont gérées en local avec SQLite.

## Structure du projet

* `main.py` : Fichier principal côté **client**.
* `server.py` : Fichier principal côté **serveur**.

## Instructions de lancement

### Serveur

Le serveur doit être lancé **depuis le dossier `src/`** :

```bash
cd src
python server.py
```

### Client

Le client doit être lancé **depuis le dossier parent de `src/`** :

```bash
python -m src.main
```

## Modules utilisés

* `PyQt6` – pour l'interface graphique
* `json` – pour la sérialisation des données
* `socket` – pour la communication réseau
* `sqlite3` – pour la base de données locale
* `dataclasses` – pour des structures de données simples et lisibles
* `datetime` – pour la gestion des dates et heures

---

Souhaites-tu que j’ajoute une section pour les prérequis ou l’installation des dépendances ?
