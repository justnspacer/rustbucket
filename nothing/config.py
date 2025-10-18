"""Configuration settings for Nothing app."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Statements directory
STATEMENTS_DIR = BASE_DIR / "statements"

# Output directory for reports and visualizations
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Transaction categories
CATEGORIES = {
    'food': ['dunkin', 'chipotle', 'portillos', 'mcdonalds', 'panda express', 'taco bell',
             'dominos', 'jimmy johns', 'guzman', 'roti', 'restaurant', 'cafe', 'coffee', 
             'food', 'grocery', 'uber eats', 'doordash', 'grubhub', 'cheesecake',
             'jersey mikes', 'tonys fresh', 'jewel osco', 'costco', 'cantina', 'tacogrill', 'la hacienda', 'greek fresh', 'brew', 'dd/br', 'chick-fil-a'],
    'transportation': ['uber', 'lyft', 'gas', 'parking', 'transit', 'metro', 'tollway',
                      'thorntons', 'exxon', 'caseys', '7-eleven', 'bp#', 'atm'],
    'entertainment': ['spotify', 'netflix', 'hulu', 'disney', 'movie', 'theater', 'game',
                     'fandango', 'peacock', 'playstation', 'xbox', 'prime video', 'audible'],
    'shopping': ['amazon', 'target', 'walmart', 'store', 'mall', 'best buy', 'hot topic',
                'earthbound', 'tnf', 'card purchase', 'hardware', 'home depot', 'lowes'],
    'utilities': ['electric', 'water', 'internet', 'phone', 'verizon', 'at&t', 'comcast',
                 'xfinity', 'nicor gas', 'water coffee delivery', 'simplisafe', 'payment sent'],
    'health': ['pharmacy', 'cvs', 'walgreens', 'doctor', 'hospital', 'clinic', 'anicca float'],
    'travel': ['hotel', 'airbnb', 'airline', 'flight', 'park chicago'],
    'services': ['github', 'google', 'microsoft', 'name-cheap', 'namecheap', 'befunky'],
}

# Date format for parsing
DATE_FORMAT = "%m/%d/%Y"
