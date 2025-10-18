# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Bot tokeni - TO'G'RILANDI
BOT_TOKEN = os.getenv('BOT_TOKEN')  # .env faylida BOT_TOKEN=7995099850:AAFaan-VTbWJtuDKVLQoL4Yk4nLVCz7jxgU

# Admin ID
ADMIN_ID = 5371043130

# Database fayl
DB_FILE = "data/anime_battle.db"

# Valyuta boshlang'ich qiymatlari
STARTING_ANICOIN = 100
STARTING_JETON = 1
STARTING_BATTLECOIN = 0
STARTING_KEYS = 0

# Jang sozlamalari
BATTLE_TIMEOUT = 30  # sekund
MAX_TEAM_SIZE = 3

# Element advantages
ELEMENT_ADVANTAGES = {
    "fire": "wind",
    "wind": "earth", 
    "earth": "water",
    "water": "fire",
    "light": "dark",
    "dark": "light"
}

# Rarity multipliers
RARITY_MULTIPLIERS = {
    "common": 1.0,
    "rare": 1.3,
    "epic": 1.7,
    "legendary": 2.2,
    "mythical": 3.0
}