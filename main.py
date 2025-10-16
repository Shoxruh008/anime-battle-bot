import logging
import sqlite3
import random
import os
import asyncio
from typing import Dict, List, Optional, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Log konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = "7995099850:AAFaan-VTbWJtuDKVLQoL4Yk4nLVCz7jxgU"

# Ma'lumotlar bazasi fayli
DB_FILE = "anime_battle_v2.db"

# Tillar
LANGUAGES = {
    "uz": "O'zbekcha",
    "ru": "Русский", 
    "en": "English"
}

# Elementlar
ELEMENTS = {
    "Fire": {"strong_against": "Wind", "weak_against": "Water", "emoji": "🔥"},
    "Water": {"strong_against": "Fire", "weak_against": "Lightning", "emoji": "💧"},
    "Wind": {"strong_against": "Earth", "weak_against": "Fire", "emoji": "🌪️"},
    "Earth": {"strong_against": "Lightning", "weak_against": "Wind", "emoji": "🌍"},
    "Lightning": {"strong_against": "Water", "weak_against": "Earth", "emoji": "⚡"},
    "Light": {"strong_against": "Dark", "weak_against": "Dark", "emoji": "✨"},
    "Dark": {"strong_against": "Light", "weak_against": "Light", "emoji": "🌑"}
}

# Tarjima matnlari
TEXTS = {
    "uz": {
        "welcome": "🎌 Anime Battle Botga xush kelibsiz, {name}!",
        "menu": "Quyidagi menyudan harakatni tanlang:",
        "get_cards": "🌼 Karta olish",
        "start_battle": "⚔️ Jangni boshlash", 
        "my_cards": "🧳 Mening kartalarim",
        "arena": "🏟️ Arena",
        "profile": "🎒 Profil",
        "clans": "🛡️ Klanlar",
        "shop": "🛍️ Do'kon",
        "main_menu": "📜 Asosiy menyu",
        "back": "🔙 Orqaga",
        "language": "🌐 Tilni tanlang",
        "settings": "⚙️ Sozlamalar",
        "help": "❓ Yordam",
        
        "starter_cards": "🎉 Tabriklaymiz! Siz boshlang'ich kartalarni oldingiz:",
        "already_have_cards": "🎴 Sizda allaqachon boshlang'ich kartalar mavjud!",
        "use_shop": "Yangi kartalar olish uchun '🛍️ Doʻkon' tugmasidan foydalaning.",
        "balance": "💰 Hisobingiz: {balance} tanga",
        
        "player_profile": "🎒 **OʻYINCHI PROFILI**",
        "player": "👤 **Oʻyinchi:**",
        "player_id": "🏷️ **ID:**",
        "balance_text": "💰 **Balans:**",
        "battle_stats": "📊 **Jang statistikasi:**",
        "wins": "🎯 Gʻalabalar:",
        "losses": "💔 Magʻlubiyatlar:",
        "win_rate": "📈 Gʻalaba foizi:",
        "card_collection": "🎴 **Karta kolleksiyasi:**",
        "total_cards": "📦 Jami kartalar:",
        "legendary": "⭐ Afsonaviy:",
        "epic": "🎭 Epik:",
        "rare": "🔵 Nadir:",
        "common": "⚪ Oddiy:",
        
        "need_3_cards": "❌ Jang boshlash uchun kamida 3 ta karta kerak.",
        "battle_started": "⚔️ **JANG BOSHlandi!**",
        "round": "**Raund {round}:**",
        "attacks": "{attacker} {defender} ga hujum qildi",
        "crit": "💥(KRITIK!)",
        "element": "⚡(Element!)",
        "defends": "{defender} himoya qildi 🛡️",
        "final_result": "**YAKUNIY NATIJA:**",
        "your_hp": "❤️ Sizning HP:",
        "cpu_hp": "❤️ CPU HP:",
        "victory": "🎉 **GʻALABA!** Siz yutdingiz va {reward} tanga oldingiz!",
        "defeat": "💔 **MAGʻLUBIYAT!** Siz yutqazdingiz, lekin {reward} tanga oldingiz.",
        "draw": "🤝 **DURRANG!** Siz {reward} tanga oldingiz.",
        
        "shop": "🛍️ **DOʻKON**",
        "your_balance": "💰 Sizning balansingiz: {balance} tanga",
        "available_packs": "**Mavjud toʻplamlar:**",
        "starter_pack": "📦 **Boshlangʻich toʻplam** - 100 tanga",
        "premium_pack": "🎁 **Premium toʻplam** - 500 tanga", 
        "legendary_pack": "💎 **Afsonaviy toʻplam** - 2000 tanga",
        "element_pack": "⚡ **Element toʻplam** - 300 tanga",
        "not_enough_coins": "❌ Tangalar yetarli emas! Kerak: {cost}💰, Sizda: {balance}💰",
        "bought_pack": "🎉 Siz {pack_type} toʻplamini {cost}💰 ga sotib oldingiz",
        "received_cards": "📦 Olingan kartalar:",
        "new_balance": "💰 Yangi balans: {balance} tanga",
        
        "arena": "🏟️ **ARENA**",
        "welcome_arena": "Xush kelibsiz, {name}!",
        "available_modes": "**Mavjud rejimlar:**",
        "quick_battle": "⚔️ Tezkor jang - CPU bilan jang",
        "daily_challenges": "🎯 Kunlik mashqlar - Maxsus vazifalar",
        "ranked_battles": "🏆 Reyting janglari - (Tez orada)",
        "team_battles": "👥 Jamoa janglari - (Tez orada)",
        "your_stats": "**Sizning statistikangiz:**",
        
        "clans": "🛡️ **KLANLAR**",
        "join_clans": "Klanlarga qoʻshiling yoki oʻz klaningizni yarating!",
        "clan_features": "**Klan imkoniyatlari:**",
        "create_clan": "• Klan yaratish (1000 tanga)",
        "join_existing": "• Mavjud klanga qoʻshilish",
        "clan_wars": "• Klan janglarida qatnashish",
        "clan_bonuses": "• Klan bonuslarini olish",
        "coming_soon": "*Klan tizimi tez orada qoʻshiladi!*"
    },
    "ru": {
        "welcome": "🎌 Добро пожаловать в Anime Battle Bot, {name}!",
        "menu": "Выберите действие из меню ниже:",
        "get_cards": "🌼 Получить карту",
        "start_battle": "⚔️ Начать бой",
        "my_cards": "🧳 Мои карты", 
        "arena": "🏟️ Арена",
        "profile": "🎒 Профиль",
        "clans": "🛡️ Кланы",
        "shop": "🛍️ Магазин",
        "main_menu": "📜 Меню",
        "back": "🔙 Назад",
        "language": "🌐 Выберите язык",
        "settings": "⚙️ Настройки",
        "help": "❓ Помощь",
        
        "starter_cards": "🎉 Поздравляем! Вы получили стартовые карты:",
        "already_have_cards": "🎴 У вас уже есть стартовые карты!",
        "use_shop": "Используйте кнопку '🛍️ Магазин' для покупки новых карт.",
        "balance": "💰 Баланс: {balance} монет",
        
        "player_profile": "🎒 **ПРОФИЛЬ ИГРОКА**",
        "player": "👤 **Игрок:**",
        "player_id": "🏷️ **ID:**", 
        "balance_text": "💰 **Баланс:**",
        "battle_stats": "📊 **Статистика битв:**",
        "wins": "🎯 Побед:",
        "losses": "💔 Поражений:",
        "win_rate": "📈 Винрейт:",
        "card_collection": "🎴 **Коллекция карт:**",
        "total_cards": "📦 Всего карт:",
        "legendary": "⭐ Легендарных:",
        "epic": "🎭 Эпических:",
        "rare": "🔵 Редких:",
        "common": "⚪ Обычных:",
        
        "need_3_cards": "❌ Для начала боя нужно как минимум 3 карты.",
        "battle_started": "⚔️ **БИТВА НАЧАЛАСЬ!**",
        "round": "**Раунд {round}:**",
        "attacks": "{attacker} атакует {defender}",
        "crit": "💥(КРИТ!)",
        "element": "⚡(Элемент!)", 
        "defends": "{defender} защищается 🛡️",
        "final_result": "**ФИНАЛЬНЫЙ РЕЗУЛЬТАТ:**",
        "your_hp": "❤️ Ваше HP:",
        "cpu_hp": "❤️ HP CPU:",
        "victory": "🎉 **ПОБЕДА!** Вы победили и получили {reward} монет!",
        "defeat": "💔 **ПОРАЖЕНИЕ!** Вы проиграли, но получили {reward} монет.",
        "draw": "🤝 **НИЧЬЯ!** Вы получили {reward} монет.",
        
        "shop": "🛍️ **МАГАЗИН**",
        "your_balance": "💰 Ваш баланс: {balance} монет",
        "available_packs": "**Доступные наборы:**",
        "starter_pack": "📦 **Стартовый набор** - 100 монет",
        "premium_pack": "🎁 **Премиум набор** - 500 монет",
        "legendary_pack": "💎 **Легендарный набор** - 2000 монет", 
        "element_pack": "⚡ **Набор элемента** - 300 монет",
        "not_enough_coins": "❌ Недостаточно монет! Нужно: {cost}💰, У вас: {balance}💰",
        "bought_pack": "🎉 Вы купили {pack_type} набор за {cost}💰",
        "received_cards": "📦 Полученные карты:",
        "new_balance": "💰 Новый баланс: {balance} монет",
        
        "arena": "🏟️ **АРЕНА**",
        "welcome_arena": "Приветствуем, {name}!",
        "available_modes": "**Доступные режимы:**",
        "quick_battle": "⚔️ Быстрый бой - Сражение с CPU",
        "daily_challenges": "🎯 Ежедневные испытания - Особые задания", 
        "ranked_battles": "🏆 Рейтинговые бои - (скоро)",
        "team_battles": "👥 Командные битвы - (скоро)",
        "your_stats": "**Ваша статистика:**",
        
        "clans": "🛡️ **КЛАНЫ**",
        "join_clans": "Присоединяйтесь к кланам или создавайте свои!",
        "clan_features": "**Возможности кланов:**",
        "create_clan": "• Создать клан (1000 монет)",
        "join_existing": "• Присоединиться к существующему клану",
        "clan_wars": "• Участвовать в клановых войнах", 
        "clan_bonuses": "• Получать клановые бонусы",
        "coming_soon": "*Клановая система будет добавлена в следующем обновлении!*"
    },
    "en": {
        "welcome": "🎌 Welcome to Anime Battle Bot, {name}!",
        "menu": "Choose an action from the menu below:",
        "get_cards": "🌼 Get Cards",
        "start_battle": "⚔️ Start Battle",
        "my_cards": "🧳 My Cards",
        "arena": "🏟️ Arena", 
        "profile": "🎒 Profile",
        "clans": "🛡️ Clans",
        "shop": "🛍️ Shop",
        "main_menu": "📜 Main Menu",
        "back": "🔙 Back",
        "language": "🌐 Choose Language",
        "settings": "⚙️ Settings",
        "help": "❓ Help",
        
        "starter_cards": "🎉 Congratulations! You received starter cards:",
        "already_have_cards": "🎴 You already have starter cards!",
        "use_shop": "Use the '🛍️ Shop' button to buy new cards.",
        "balance": "💰 Balance: {balance} coins",
        
        "player_profile": "🎒 **PLAYER PROFILE**",
        "player": "👤 **Player:**",
        "player_id": "🏷️ **ID:**",
        "balance_text": "💰 **Balance:**", 
        "battle_stats": "📊 **Battle Statistics:**",
        "wins": "🎯 Wins:",
        "losses": "💔 Losses:",
        "win_rate": "📈 Win Rate:",
        "card_collection": "🎴 **Card Collection:**",
        "total_cards": "📦 Total Cards:",
        "legendary": "⭐ Legendary:",
        "epic": "🎭 Epic:",
        "rare": "🔵 Rare:",
        "common": "⚪ Common:",
        
        "need_3_cards": "❌ You need at least 3 cards to start a battle.",
        "battle_started": "⚔️ **BATTLE STARTED!**",
        "round": "**Round {round}:**",
        "attacks": "{attacker} attacks {defender}",
        "crit": "💥(CRIT!)",
        "element": "⚡(Element!)",
        "defends": "{defender} defends 🛡️", 
        "final_result": "**FINAL RESULT:**",
        "your_hp": "❤️ Your HP:",
        "cpu_hp": "❤️ CPU HP:",
        "victory": "🎉 **VICTORY!** You won and received {reward} coins!",
        "defeat": "💔 **DEFEAT!** You lost but received {reward} coins.",
        "draw": "🤝 **DRAW!** You received {reward} coins.",
        
        "shop": "🛍️ **SHOP**",
        "your_balance": "💰 Your balance: {balance} coins",
        "available_packs": "**Available Packs:**",
        "starter_pack": "📦 **Starter Pack** - 100 coins",
        "premium_pack": "🎁 **Premium Pack** - 500 coins",
        "legendary_pack": "💎 **Legendary Pack** - 2000 coins",
        "element_pack": "⚡ **Element Pack** - 300 coins", 
        "not_enough_coins": "❌ Not enough coins! Need: {cost}💰, You have: {balance}💰",
        "bought_pack": "🎉 You bought {pack_type} pack for {cost}💰",
        "received_cards": "📦 Received cards:",
        "new_balance": "💰 New balance: {balance} coins",
        
        "arena": "🏟️ **ARENA**",
        "welcome_arena": "Welcome, {name}!",
        "available_modes": "**Available Modes:**",
        "quick_battle": "⚔️ Quick Battle - Fight against CPU",
        "daily_challenges": "🎯 Daily Challenges - Special tasks",
        "ranked_battles": "🏆 Ranked Battles - (Coming soon)", 
        "team_battles": "👥 Team Battles - (Coming soon)",
        "your_stats": "**Your Statistics:**",
        
        "clans": "🛡️ **CLANS**",
        "join_clans": "Join clans or create your own!",
        "clan_features": "**Clan Features:**",
        "create_clan": "• Create clan (1000 coins)",
        "join_existing": "• Join existing clan", 
        "clan_wars": "• Participate in clan wars",
        "clan_bonuses": "• Receive clan bonuses",
        "coming_soon": "*Clan system will be added in the next update!*"
    }
}

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self._init_database()
    
    def _init_database(self):
        """Ma'lumotlar bazasini ishga tushirish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Foydalanuvchilar jadvali
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    balance INTEGER DEFAULT 1000,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    language TEXT DEFAULT 'uz',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Personajlar jadvali
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    element TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    base_hp INTEGER NOT NULL,
                    base_attack INTEGER NOT NULL,
                    base_defense INTEGER NOT NULL,
                    base_speed INTEGER NOT NULL,
                    price INTEGER NOT NULL
                )
            ''')
            
            # Foydalanuvchi kartalari
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    character_id INTEGER NOT NULL,
                    level INTEGER DEFAULT 1,
                    experience INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (character_id) REFERENCES characters (id)
                )
            ''')
            
            # Janglar tarixi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS battles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    result TEXT NOT NULL,
                    reward INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Standart personajlarni qo'shish
            default_characters = [
                (1, "Naruto Uzumaki", "Wind", "Legendary", 1200, 180, 80, 120, 10000),
                (2, "Sasuke Uchiha", "Lightning", "Legendary", 1100, 190, 70, 125, 10000),
                (3, "Goku", "Light", "Legendary", 1500, 200, 90, 130, 15000),
                (4, "Luffy", "Fire", "Legendary", 1300, 170, 60, 110, 12000),
                (5, "Levi Ackerman", "Wind", "Legendary", 1000, 160, 75, 140, 11000),
                (6, "Vegeta", "Fire", "Epic", 900, 150, 85, 115, 5000),
                (7, "Zoro", "Earth", "Epic", 950, 145, 80, 100, 4500),
                (8, "Eren Yeager", "Dark", "Epic", 850, 140, 70, 105, 4000),
                (9, "Gon Freecss", "Light", "Rare", 750, 130, 68, 108, 1500),
                (10, "Killua Zoldyck", "Lightning", "Rare", 720, 128, 66, 135, 1600),
                (11, "Edward Elric", "Earth", "Rare", 780, 125, 75, 95, 1400),
                (12, "Spike Spiegel", "Fire", "Rare", 700, 122, 64, 112, 1300),
                (13, "Sailor Moon", "Light", "Epic", 820, 138, 74, 104, 3500),
                (14, "Monkey D. Dragon", "Wind", "Epic", 890, 144, 76, 98, 4600),
                (15, "Mikasa Ackerman", "Wind", "Rare", 680, 135, 62, 120, 1700)
            ]
            
            cursor.executemany('''
                INSERT OR IGNORE INTO characters 
                (id, name, element, rarity, base_hp, base_attack, base_defense, base_speed, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', default_characters)
            
            conn.commit()
            conn.close()
            print("✅ Ma'lumotlar bazasi muvaffaqiyatli ishga tushirildi")
        except Exception as e:
            print(f"❌ Ma'lumotlar bazasini ishga tushirishda xatolik: {e}")
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchini olish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "user_id": user[0],
                    "username": user[1],
                    "balance": user[2],
                    "wins": user[3],
                    "losses": user[4],
                    "language": user[5],
                    "created_at": user[6]
                }
            return None
        except Exception as e:
            print(f"❌ Foydalanuvchini olishda xatolik: {e}")
            return None
    
    def create_user(self, user_id: int, username: str, language: str = 'uz'):
        """Yangi foydalanuvchi yaratish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username, language) VALUES (?, ?, ?)",
                (user_id, username, language)
            )
            conn.commit()
            conn.close()
            print(f"✅ Yangi foydalanuvchi yaratildi: {user_id}")
        except Exception as e:
            print(f"❌ Foydalanuvchi yaratishda xatolik: {e}")
    
    def update_balance(self, user_id: int, amount: int):
        """Balansni yangilash"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Balansni yangilashda xatolik: {e}")
    
    def update_language(self, user_id: int, language: str):
        """Tilni yangilash"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Tilni yangilashda xatolik: {e}")
    
    def update_stats(self, user_id: int, win: bool):
        """Statistikani yangilash"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            if win:
                cursor.execute("UPDATE users SET wins = wins + 1 WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("UPDATE users SET losses = losses + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Statistikani yangilashda xatolik: {e}")
    
    def get_random_characters(self, count: int = 3, rarity: str = None) -> List[Dict]:
        """Tasodifiy personajlarni olish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if rarity:
                cursor.execute(
                    "SELECT * FROM characters WHERE rarity = ? ORDER BY RANDOM() LIMIT ?",
                    (rarity, count)
                )
            else:
                cursor.execute("SELECT * FROM characters ORDER BY RANDOM() LIMIT ?", (count,))
            
            characters = cursor.fetchall()
            conn.close()
            
            return [{
                "id": char[0],
                "name": char[1],
                "element": char[2],
                "rarity": char[3],
                "base_hp": char[4],
                "base_attack": char[5],
                "base_defense": char[6],
                "base_speed": char[7],
                "price": char[8]
            } for char in characters]
        except Exception as e:
            print(f"❌ Personajlarni olishda xatolik: {e}")
            return []
    
    def add_user_character(self, user_id: int, character_id: int):
        """Foydalanuvchiga karta qo'shish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_characters (user_id, character_id) VALUES (?, ?)",
                (user_id, character_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Karta qo'shishda xatolik: {e}")
    
    def get_user_characters(self, user_id: int) -> List[Dict]:
        """Foydalanuvchi kartalarini olish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, uc.level, uc.experience 
                FROM characters c
                JOIN user_characters uc ON c.id = uc.character_id
                WHERE uc.user_id = ?
            ''', (user_id,))
            characters = cursor.fetchall()
            conn.close()
            
            return [{
                "id": char[0],
                "name": char[1],
                "element": char[2],
                "rarity": char[3],
                "hp": char[4],
                "attack": char[5],
                "defense": char[6],
                "speed": char[7],
                "price": char[8],
                "level": char[9],
                "experience": char[10]
            } for char in characters]
        except Exception as e:
            print(f"❌ Kartalarni olishda xatolik: {e}")
            return []
    
    def add_battle_record(self, user_id: int, result: str, reward: int):
        """Jang yozuvini qo'shish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO battles (user_id, result, reward) VALUES (?, ?, ?)",
                (user_id, result, reward)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Jang yozuvini qo'shishda xatolik: {e}")

# Database obyektini yaratish
db = Database(DB_FILE)

# Asosiy menyu tugmalari (Rasmdagidek joylashuv)
def get_main_keyboard(language: str = 'uz'):
    texts = TEXTS[language]
    
    keyboard = [
        [KeyboardButton(texts["get_cards"]), KeyboardButton(texts["get_cards"])],
        [KeyboardButton(texts["my_cards"])],
        [KeyboardButton(texts["arena"]), KeyboardButton(texts["profile"]), KeyboardButton(texts["clans"])],
        [KeyboardButton(texts["shop"]), KeyboardButton(texts["main_menu"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Sozlamalar tugmalari
def get_settings_keyboard(language: str = 'uz'):
    texts = TEXTS[language]
    
    keyboard = [
        [InlineKeyboardButton(texts["language"], callback_data="settings_language")],
        [InlineKeyboardButton(texts["help"], callback_data="settings_help")],
        [InlineKeyboardButton(texts["back"], callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Til tanlash tugmalari
def get_language_keyboard():
    keyboard = []
    for lang_code, lang_name in LANGUAGES.items():
        keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"set_language_{lang_code}")])
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_settings")])
    return InlineKeyboardMarkup(keyboard)

# Do'kon tugmalari
def get_shop_keyboard(language: str = 'uz'):
    texts = TEXTS[language]
    
    keyboard = [
        [InlineKeyboardButton(texts["starter_pack"], callback_data="shop_starter")],
        [InlineKeyboardButton(texts["premium_pack"], callback_data="shop_premium")],
        [InlineKeyboardButton(texts["legendary_pack"], callback_data="shop_legendary")],
        [InlineKeyboardButton(texts["element_pack"], callback_data="shop_element")],
        [InlineKeyboardButton(texts["back"], callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Jang mexanikasi
class BattleSystem:
    @staticmethod
    def calculate_damage(attacker: Dict, defender: Dict) -> Tuple[int, bool, bool]:
        """Zararni hisoblash"""
        base_damage = attacker["attack"] - (defender["defense"] * 0.3)
        base_damage = max(10, base_damage)
        
        # Element ustunligi
        element_bonus = 1.0
        element_advantage = False
        if ELEMENTS[attacker["element"]]["strong_against"] == defender["element"]:
            element_bonus = 1.3
            element_advantage = True
        
        # Critical hit
        critical = random.random() < 0.1
        critical_multiplier = 1.5 if critical else 1.0
        
        final_damage = int(base_damage * element_bonus * critical_multiplier)
        
        return final_damage, critical, element_advantage
    
    @staticmethod
    def cpu_decision(cpu_char: Dict, user_char: Dict) -> str:
        """CPU qaror qabul qilish"""
        hp_ratio = cpu_char["hp"] / cpu_char["base_hp"]
        
        # Agar HP past bo'lsa, himoya qilish
        if hp_ratio < 0.3:
            if random.random() < 0.7:
                return "defend"
        
        # Element ustunligi bo'lsa, hujum qilish
        if ELEMENTS[cpu_char["element"]]["strong_against"] == user_char["element"]:
            if random.random() < 0.8:
                return "attack"
        
        # Aks holda tasodifiy harakat
        return random.choice(["attack", "defend"])

# Bot komandalari
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Foydalanuvchini yaratish yoki olish
    user_data = db.get_user(user.id)
    if not user_data:
        db.create_user(user.id, user.first_name or "User")
        user_data = db.get_user(user.id)
    
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    welcome_text = f"""
{texts['welcome'].format(name=user.first_name)}

Bu yerda siz:
• Anime personaj kartalarini to'plashingiz mumkin
• Epik janglarda qatnashishingiz mumkin
• Qahramonlaringizni rivojlantirishingiz mumkin
• Do'stlaringiz bilan klanlar tuzishingiz mumkin

{texts['menu']}
    """
    
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard(language))

async def get_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Foydalanuvchini tekshirish
    user_data = db.get_user(user.id)
    if not user_data:
        db.create_user(user.id, user.first_name or "User")
        user_data = db.get_user(user.id)
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    user_cards = db.get_user_characters(user.id)
    
    if len(user_cards) == 0:
        # Boshlang'ich kartalar berish
        random_chars = db.get_random_characters(3)
        for char in random_chars:
            db.add_user_character(user.id, char["id"])
        
        char_list = "\n".join([f"• {char['name']} ({char['rarity']}) - {char['element']}" for char in random_chars])
        text = f"""
{texts['starter_cards']}

{char_list}

{texts['balance'].format(balance=user_data['balance'])}
{texts['use_shop']}
        """
    else:
        text = f"""
{texts['already_have_cards']}

{texts['balance'].format(balance=user_data['balance'])}
{texts['use_shop']}
        """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def my_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    user_cards = db.get_user_characters(user.id)
    
    if not user_cards:
        text = f"❌ {texts['need_3_cards']} '{texts['get_cards']}' tugmasi orqali boshlang'ich kartalarni oling!"
    else:
        text = f"🧳 **{texts['my_cards']}:**\n\n"
        for i, card in enumerate(user_cards, 1):
            element_emoji = ELEMENTS[card["element"]]["emoji"]
            
            rarity_emojis = {
                "Common": "⚪", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟡"
            }
            
            text += f"""
{i}. {rarity_emojis[card['rarity']]} **{card['name']}** {element_emoji}
   ⚡ Daraja: {card['level']} | 🎭 {card['element']} | ⭐ {card['rarity']}
   ❤️ HP: {card['hp']} | ⚔️ Hujum: {card['attack']} 
   🛡️ Himoya: {card['defense']} | 🏃 Tezlik: {card['speed']}
────────────────
            """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    user_cards = db.get_user_characters(user.id)
    
    if len(user_cards) < 3:
        text = f"❌ {texts['need_3_cards']} '{texts['get_cards']}' orqali kartalarni oling!"
        await update.message.reply_text(text, reply_markup=get_main_keyboard(language))
        return
    
    # User jamoasi (birinchi 3 ta karta)
    user_team = user_cards[:3]
    
    # CPU jamoasini yaratish
    cpu_team = []
    for _ in range(3):
        cpu_char = db.get_random_characters(1)[0]
        cpu_team.append({
            **cpu_char,
            "current_hp": cpu_char["base_hp"]
        })
    
    # Jangni boshlash
    battle_log = [f"⚔️ **{texts['battle_started']}**\n"]
    
    # Roundlar
    for round_num in range(1, 6):
        battle_log.append(f"\n**{texts['round'].format(round=round_num)}**")
        
        # Har bir personaj uchun harakat
        for i in range(3):
            user_char = user_team[i]
            cpu_char = cpu_team[i]
            
            # Agar personajlar tirik bo'lsa
            if user_char["hp"] > 0 and cpu_char["current_hp"] > 0:
                # User harakati
                damage, critical, element_advantage = BattleSystem.calculate_damage(user_char, cpu_char)
                cpu_char["current_hp"] = max(0, cpu_char["current_hp"] - damage)
                
                log_entry = f"• {texts['attacks'].format(attacker=user_char['name'], defender=cpu_char['name'])}"
                if critical:
                    log_entry += f" {texts['crit']}"
                if element_advantage:
                    log_entry += f" {texts['element']}"
                log_entry += f" -{damage} HP"
                
                battle_log.append(log_entry)
                
                # CPU harakati
                if cpu_char["current_hp"] > 0:
                    cpu_action = BattleSystem.cpu_decision(cpu_char, user_char)
                    
                    if cpu_action == "attack":
                        damage, critical, element_advantage = BattleSystem.calculate_damage(cpu_char, user_char)
                        user_char["hp"] = max(0, user_char["hp"] - damage)
                        
                        log_entry = f"• {texts['attacks'].format(attacker=cpu_char['name'], defender=user_char['name'])}"
                        if critical:
                            log_entry += f" {texts['crit']}"
                        if element_advantage:
                            log_entry += f" {texts['element']}"
                        log_entry += f" -{damage} HP"
                        
                        battle_log.append(log_entry)
                    else:
                        battle_log.append(f"• {texts['defends'].format(defender=cpu_char['name'])}")
        
        # Jang tugashini tekshirish
        user_alive = any(char["hp"] > 0 for char in user_team)
        cpu_alive = any(char["current_hp"] > 0 for char in cpu_team)
        
        if not user_alive or not cpu_alive:
            break
    
    # Jang natijasini aniqlash
    user_final_hp = sum(char["hp"] for char in user_team)
    cpu_final_hp = sum(char["current_hp"] for char in cpu_team)
    
    if user_final_hp > cpu_final_hp:
        result = "win"
        reward = random.randint(80, 150)
        db.update_balance(user.id, reward)
        db.update_stats(user.id, True)
        result_text = texts['victory'].format(reward=reward)
    elif user_final_hp < cpu_final_hp:
        result = "loss"
        reward = random.randint(20, 50)
        db.update_balance(user.id, reward)
        db.update_stats(user.id, False)
        result_text = texts['defeat'].format(reward=reward)
    else:
        result = "draw"
        reward = random.randint(30, 70)
        db.update_balance(user.id, reward)
        result_text = texts['draw'].format(reward=reward)
    
    # Jang yozuvini qo'shish
    db.add_battle_record(user.id, result, reward)
    
    battle_report = f"""
{"".join(battle_log)}

**{texts['final_result']}**
{texts['your_hp']} {user_final_hp}
{texts['cpu_hp']} {cpu_final_hp}

{result_text}
    """
    
    await update.message.reply_text(battle_report, reply_markup=get_main_keyboard(language))

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    user_cards = db.get_user_characters(user.id)
    total_battles = user_data["wins"] + user_data["losses"]
    win_rate = (user_data["wins"] / total_battles * 100) if total_battles > 0 else 0
    
    # Karta statistikasi
    rarity_count = {"Common": 0, "Rare": 0, "Epic": 0, "Legendary": 0}
    for card in user_cards:
        rarity_count[card["rarity"]] += 1
    
    text = f"""
{texts['player_profile']}

{texts['player']} {user.first_name}
{texts['player_id']} {user.id}
{texts['balance_text']} {user_data['balance']} tanga

{texts['battle_stats']}
{texts['wins']} {user_data['wins']}
{texts['losses']} {user_data['losses']}
{texts['win_rate']} {win_rate:.1f}%

{texts['card_collection']}
{texts['total_cards']} {len(user_cards)}
{texts['legendary']} {rarity_count['Legendary']}
{texts['epic']} {rarity_count['Epic']}
{texts['rare']} {rarity_count['Rare']}
{texts['common']} {rarity_count['Common']}
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def arena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    text = f"""
{texts['arena']}

{texts['welcome_arena'].format(name=user.first_name)} 

**{texts['available_modes']}**

{texts['quick_battle']}
{texts['daily_challenges']}
{texts['ranked_battles']}
{texts['team_battles']}

**{texts['your_stats']}**
{texts['balance_text']} {user_data['balance']} tanga
{texts['wins']} {user_data['wins']}
{texts['losses']} {user_data['losses']}

'{texts['start_battle']}' tugmasi orqali tezkor jangni boshlang!
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def clans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    text = f"""
{texts['clans']}

{texts['join_clans']}

**{texts['clan_features']}**
{texts['create_clan']}
{texts['join_existing']}
{texts['clan_wars']}
{texts['clan_bonuses']}

{texts['coming_soon']}

Hozircha siz:
• Kartalarni to'plash 🌼
• Janglarga qatnashish ⚔️
• Koleksiyangizni yaxshilash 🧳
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    text = f"""
{texts['shop']}

{texts['your_balance'].format(balance=user_data['balance'])}

**{texts['available_packs']}**

{texts['starter_pack']}
• 3 ta tasodifiy karta (Common/Rare)
• Epik karta olish imkoniyati: 10%

{texts['premium_pack']}  
• 5 ta karta (1 ta Epik karta kafolatlangan)
• Afsonaviy karta olish imkoniyati: 5%

{texts['legendary_pack']}
• 3 ta karta (1 ta Afsonaviy karta kafolatlangan)
• Maksimal xususiyatlar

{texts['element_pack']}
• 3 ta bir xil elementdagi karta
    """
    
    await update.message.reply_text(text, reply_markup=get_shop_keyboard(language))

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    text = f"""
📜 **{texts['main_menu']}**

**Oʻyin funksiyalari:**
🎮 Asosiy rejimlar
🎴 Karta kolleksiyasi
⚔️ Jang tizimi
🛍️ Doʻkon

**Tez orada:**
🏆 Reyting janglari
👥 Klanlar
🎯 Kunlik vazifalar
🏅 Yutuqlar

**Qoʻllab-quvvatlash:**
📖 Oʻyin qoidalari
❓ Yordam
🔧 Sozlamalar

Bogʻlanish uchun: @admin
    """
    
    keyboard = [
        [InlineKeyboardButton(texts['settings'], callback_data="settings_menu")],
        [InlineKeyboardButton(texts['help'], callback_data="settings_help")],
        [InlineKeyboardButton(texts['back'], callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

# Callback query handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await query.edit_message_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    data = query.data
    
    if data.startswith("shop_"):
        if data == "shop_starter":
            cost = 100
            pack_type = "boshlang'ich"
            chars = db.get_random_characters(3)
        elif data == "shop_premium":
            cost = 500
            pack_type = "premium"
            epic_char = db.get_random_characters(1, "Epic")[0]
            other_chars = db.get_random_characters(4)
            chars = [epic_char] + other_chars
        elif data == "shop_legendary":
            cost = 2000
            pack_type = "afsonaviy"
            legendary_char = db.get_random_characters(1, "Legendary")[0]
            other_chars = db.get_random_characters(2)
            chars = [legendary_char] + other_chars
        elif data == "shop_element":
            cost = 300
            pack_type = "element"
            elements = list(ELEMENTS.keys())
            random_element = random.choice(elements)
            chars = db.get_random_characters(3)
            for char in chars:
                char["element"] = random_element
        else:
            return
        
        if user_data["balance"] < cost:
            await query.edit_message_text(
                texts['not_enough_coins'].format(cost=cost, balance=user_data['balance']),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(texts['back'], callback_data="back_to_shop")]])
            )
            return
        
        # Xaridni amalga oshirish
        db.update_balance(user.id, -cost)
        
        for char in chars:
            db.add_user_character(user.id, char["id"])
        
        char_list = "\n".join([f"• {char['name']} ({char['rarity']}) - {char['element']}" for char in chars])
        new_balance = user_data['balance'] - cost
        
        await query.edit_message_text(
            f"""{texts['bought_pack'].format(pack_type=pack_type, cost=cost)}

{texts['received_cards']}
{char_list}

{texts['new_balance'].format(balance=new_balance)}""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛍️ " + texts['shop'], callback_data="back_to_shop")]])
        )
    
    elif data == "settings_menu":
        await query.edit_message_text(
            "⚙️ **Sozlamalar**\n\nQuyidagi sozlamalarni o'zgartirishingiz mumkin:",
            reply_markup=get_settings_keyboard(language)
        )
    
    elif data == "settings_language":
        await query.edit_message_text(
            "🌐 **Tilni tanlang**:",
            reply_markup=get_language_keyboard()
        )
    
    elif data.startswith("set_language_"):
        new_language = data.replace("set_language_", "")
        db.update_language(user.id, new_language)
        
        new_texts = TEXTS[new_language]
        await query.edit_message_text(
            f"✅ Til o'zgartirildi: {LANGUAGES[new_language]}\n\n{new_texts['menu']}",
            reply_markup=get_main_keyboard(new_language)
        )
    
    elif data == "settings_help":
        help_text = """
❓ **Yordam**

**Qanday o'ynash kerak:**
1. 🌼 Karta olish - Boshlang'ich 3 ta karta oling
2. ⚔️ Jangni boshlash - CPU bilan jang qiling
3. 🧳 Kartalaringizni ko'ring - Koleksiyangizni boshqaring
4. 🛍️ Do'kon - Yangi kartalar sotib oling

**Jang qoidalari:**
• Har bir personajning element ustunligi bor
• Critical hit - 10% ehtimollik
• Element bonus - 30% ko'proq zarar

**Kontakt:** @admin
        """
        await query.edit_message_text(
            help_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(texts['back'], callback_data="back_to_settings")]])
        )
    
    elif data in ["back_to_shop", "back_to_settings", "back_to_menu", "back_to_main"]:
        if data == "back_to_shop":
            await shop(update, context)
        elif data == "back_to_settings":
            await query.edit_message_text(
                "⚙️ **Sozlamalar**",
                reply_markup=get_settings_keyboard(language)
            )
        else:
            await query.edit_message_text(texts['menu'], reply_markup=get_main_keyboard(language))

# Xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("Iltimos, avval /start buyrug'ini bering.")
        return
    
    language = user_data["language"]
    texts = TEXTS[language]
    
    text = update.message.text
    
    if text == texts["get_cards"]:
        await get_cards(update, context)
    elif text == texts["my_cards"]:
        await my_cards(update, context)
    elif text == texts["start_battle"]:
        await start_battle(update, context)
    elif text == texts["profile"]:
        await profile(update, context)
    elif text == texts["arena"]:
        await arena(update, context)
    elif text == texts["clans"]:
        await clans(update, context)
    elif text == texts["shop"]:
        await shop(update, context)
    elif text == texts["main_menu"]:
        await main_menu(update, context)
    else:
        await update.message.reply_text(
            "Iltimos, navigatsiya qilish uchun menyu tugmalaridan foydalaning!",
            reply_markup=get_main_keyboard(language)
        )

# Asosiy funksiya
def main():
    # Eski bot instansiyalarini to'xtatish
    print("🔄 Bot ishga tushmoqda...")
    
    # Yangi ma'lumotlar bazasi fayli
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑️ Eski ma'lumotlar bazasi o'chirildi")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Anime Battle Bot ishga tushdi!")
    print("🌐 Tillar: O'zbekcha, Русский, English")
    print("🎴 15 ta personaj mavjud")
    print("⚔️ To'liq jang tizimi faol")
    print("🛍️ Do'kon tizimi ishlamoqda")
    print("💰 Iqtisodiyot tizimi ishga tushirildi")
    
    # Botni ishga tushirish
    application.run_polling()

if __name__ == "__main__":
    main()