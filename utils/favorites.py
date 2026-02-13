# utils/favorites.py
"""
Favorites management utility.
Handles saving and loading favorite cities.
"""
import json
import os

FAVORITES_FILE = "favorites.json"

def load_favorites():
    """
    Load favorite cities from file.
    
    Returns:
        list: List of favorite city names
    """
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_favorites(favorites):
    """
    Save favorite cities to file.
    
    Args:
        favorites (list): List of city names to save
    """
    try:
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f, indent=2)
    except Exception as e:
        print(f"Error saving favorites: {e}")

def add_favorite(city):
    """
    Add a city to favorites.
    
    Args:
        city (str): City name to add
    """
    favorites = load_favorites()
    if city not in favorites:
        favorites.append(city)
        save_favorites(favorites)
        return True
    return False

def remove_favorite(city):
    """
    Remove a city from favorites.
    
    Args:
        city (str): City name to remove
    """
    favorites = load_favorites()
    if city in favorites:
        favorites.remove(city)
        save_favorites(favorites)
        return True
    return False

def is_favorite(city):
    """
    Check if a city is in favorites.
    
    Args:
        city (str): City name to check
        
    Returns:
        bool: True if city is a favorite, False otherwise
    """
    return city in load_favorites()

def clear_favorites():
    """Clear all favorites."""
    save_favorites([])