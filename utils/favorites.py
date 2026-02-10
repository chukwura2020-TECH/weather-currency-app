# utils/favorites.py
"""
Manage favorite cities with persistent storage.
"""
import json
import os

FAVORITES_FILE = 'favorites.json'

def load_favorites():
    """Load favorite cities from file"""
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_favorites(favorites):
    """Save favorite cities to file"""
    try:
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f, indent=2)
        return True
    except:
        return False

def add_favorite(city):
    """Add a city to favorites"""
    favorites = load_favorites()
    if city not in favorites:
        favorites.append(city)
        save_favorites(favorites)
    return favorites

def remove_favorite(city):
    """Remove a city from favorites"""
    favorites = load_favorites()
    if city in favorites:
        favorites.remove(city)
        save_favorites(favorites)
    return favorites

def is_favorite(city):
    """Check if city is in favorites"""
    return city in load_favorites()