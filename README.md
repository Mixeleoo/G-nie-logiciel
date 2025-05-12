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

* `PyQt6`
* `json`
* `socket`
* `sqlite3`
* `dataclasses`
* `datetime`
* `abc`
