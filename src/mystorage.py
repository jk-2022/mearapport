import json
import os

STORAGE_FILE = "mystorage.json"

def load_storage():
    """Charge les données depuis le fichier JSON, ou retourne un dictionnaire vide."""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_storage(data):
    """Sauvegarde les données dans le fichier JSON."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def set_value(key, value):
    """Ajoute ou met à jour une valeur dans le storage."""
    data = load_storage()
    data[key] = value
    save_storage(data)


def get_value(key, default=None):
    """Récupère une valeur par sa clé, ou retourne 'default' si elle n'existe pas."""
    data = load_storage()
    return data.get(key, default)


def delete_value(key):
    """Supprime une valeur par sa clé si elle existe."""
    data = load_storage()
    if key in data:
        del data[key]
        save_storage(data)


def get_all():
    """Retourne toutes les données du storage."""
    return load_storage()
