import logging
import sqlite3
import json
import random
import os
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
DB_FILE = "anime_battle.db"

# Til sozlamalari
LANGUAGES = {
    "uz": "O'zbekcha",
    "ru": "Русский", 
    "en": "English"
}

# Elementlar
ELEMENTS = {
    "Fire": {"strong_against": "Wind", "weak_against": "Water"},
    "Water": {"strong_against": "Fire", "weak_against": "Lightning"},
    "Wind": {"strong_against": "Earth", "weak_against": "Fire"},
    "Earth": {"strong_against": "Lightning", "weak_against": "Wind"},
    "Lightning": {"strong_against": "Water", "weak_against": "Earth"},
    "Light": {"strong_against": "Dark", "weak_against": "Dark"},
    "Dark": {"strong_against": "Light", "weak_against": "Light"}
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
        "balance_text": "💰 **Balans:**",
        "wins": "🎯 Gʻalabalar:",
        "losses": "💔 Magʻlubiyatlar:",
        "win_rate": "📈 Gʻalaba foizi:",
        "total_cards": "📦 Jami kartalar:",
        
        "need_3_cards": "❌ Jang boshlash uchun kamida 3 ta karta kerak.",
        "victory": "🎉 **GʻALABA!** Siz yutdingiz va {reward} tanga oldingiz!",
        "defeat": "💔 **MAGʻLUBIYAT!** Siz yutqazdingiz, lekin {reward} tanga oldingiz.",
        
        "shop": "🛍️ **DOʻKON**",
        "your_balance": "💰 Sizning balansingiz: {balance} tanga",
        "starter_pack": "📦 **Boshlangʻich toʻplam** - 100 tanga",
        "premium_pack": "🎁 **Premium toʻplam** - 500 tanga", 
        "not_enough_coins": "❌ Tangalar yetarli emas! Kerak: {cost}💰, Sizda: {balance}💰",
        "bought_pack": "🎉 Siz {pack_type} toʻplamini {cost}💰 ga sotib oldingiz",
        "received_cards": "📦 Olingan kartalar:",
        "new_balance": "💰 Yangi balans: {balance} tanga",
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
        "balance_text": "💰 **Баланс:**",
        "wins": "🎯 Побед:",
        "losses": "💔 Поражений:",
        "win_rate": "📈 Винрейт:",
        "total_cards": "📦 Всего карт:",
        
        "need_3_cards": "❌ Для начала боя нужно как минимум 3 карты.",
        "victory": "🎉 **ПОБЕДА!** Вы победили и получили {reward} монет!",
        "defeat": "💔 **ПОРАЖЕНИЕ!** Вы проиграли, но получили {reward} монет.",
        
        "shop": "🛍️ **МАГАЗИН**",
        "your_balance": "💰 Ваш баланс: {balance} монет",
        "starter_pack": "📦 **Стартовый набор** - 100 монет",
        "premium_pack": "🎁 **Премиум набор** - 500 монет", 
        "not_enough_coins": "❌ Недостаточно монет! Нужно: {cost}💰, У вас: {balance}💰",
        "bought_pack": "🎉 Вы купили {pack_type} набор за {cost}💰",
        "received_cards": "📦 Полученные карты:",
        "new_balance": "💰 Новый баланс: {balance} монет",
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
        "balance_text": "💰 **Balance:**",
        "wins": "🎯 Wins:",
        "losses": "💔 Losses:",
        "win_rate": "📈 Win Rate:",
        "total_cards": "📦 Total Cards:",
        
        "need_3_cards": "❌ You need at least 3 cards to start a battle.",
        "victory": "🎉 **VICTORY!** You won and received {reward} coins!",
        "defeat": "💔 **DEFEAT!** You lost but received {reward} coins.",
        
        "shop": "🛍️ **SHOP**",
        "your_balance": "💰 Your balance: {balance} coins",
        "starter_pack": "📦 **Starter Pack** - 100 coins",
        "premium_pack": "🎁 **Premium Pack** - 500 coins", 
        "not_enough_coins": "❌ Not enough coins! Need: {cost}💰, You have: {balance}💰",
        "bought_pack": "🎉 You bought {pack_type} pack for {cost}💰",
        "received_cards": "📦 Received cards:",
        "new_balance": "💰 New balance: {balance} coins",
    }
}

class SimpleDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Ma'lumotlar bazasini ishga tushirish"""
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
                language TEXT DEFAULT 'uz'
            )
        ''')
        
        # Personajlar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                element TEXT,
                rarity TEXT,
                hp INTEGER,
                attack INTEGER,
                defense INTEGER,
                speed INTEGER
            )
        ''')
        
        # Foydalanuvchi kartalari
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                character_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(character_id) REFERENCES characters(id)
            )
        ''')
        
        # Standart personajlarni qo'shish
        default_characters = [
            (1, "Naruto Uzumaki", "Wind", "Legendary", 1200, 180, 80, 120),
            (2, "Sasuke Uchiha", "Lightning", "Legendary", 1100, 190, 70, 125),
            (3, "Goku", "Light", "Legendary", 1500, 200, 90, 130),
            (4, "Luffy", "Fire", "Legendary", 1300, 170, 60, 110),
            (5, "Levi Ackerman", "Wind", "Legendary", 1000, 160, 75, 140),
            (6, "Vegeta", "Fire", "Epic", 900, 150, 85, 115),
            (7, "Zoro", "Earth", "Epic", 950, 145, 80, 100),
            (8, "Eren Yeager", "Dark", "Epic", 850, 140, 70, 105),
            (9, "Gon Freecss", "Light", "Rare", 750, 130, 68, 108),
            (10, "Killua Zoldyck", "Lightning", "Rare", 720, 128, 66, 135)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO characters (id, name, element, rarity, hp, attack, defense, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_characters)
        
        conn.commit()
        conn.close()
        print("✅ Ma'lumotlar bazasi ishga tushirildi")
    
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
                    "language": user[5]
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
            print(f"✅ Yangi foydalanuvchi: {user_id}")
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
    
    def get_random_characters(self, count: int = 3) -> List[Dict]:
        """Tasodifiy personajlarni olish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM characters ORDER BY RANDOM() LIMIT {count}")
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
                "speed": char[7]
            } for char in characters]
        except Exception as e:
            print(f"❌ Personajlarni olishda xatolik: {e}")
            return []
    
    def add_user_card(self, user_id: int, character_id: int):
        """Foydalanuvchiga karta qo'shish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_cards (user_id, character_id) VALUES (?, ?)",
                (user_id, character_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Karta qo'shishda xatolik: {e}")
    
    def get_user_cards(self, user_id: int) -> List[Dict]:
        """Foydalanuvchi kartalarini olish"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.* FROM characters c
                JOIN user_cards uc ON c.id = uc.character_id
                WHERE uc.user_id = ?
            ''', (user_id,))
            cards = cursor.fetchall()
            conn.close()
            
            return [{
                "id": card[0],
                "name": card[1],
                "element": card[2],
                "rarity": card[3],
                "hp": card[4],
                "attack": card[5],
                "defense": card[6],
                "speed": card[7]
            } for card in cards]
        except Exception as e:
            print(f"❌ Kartalarni olishda xatolik: {e}")
            return []
    
    def update_user_stats(self, user_id: int, win: bool):
        """Foydalanuvchi statistikasini yangilash"""
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

# Database obyektini yaratish
db = SimpleDatabase(DB_FILE)

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

# Jang mexanikasi
class BattleSystem:
    @staticmethod
    def calculate_damage(attacker: Dict, defender: Dict) -> int:
        """Zararni hisoblash"""
        base_damage = attacker["attack"] - (defender["defense"] * 0.3)
        base_damage = max(10, base_damage)
        
        # Element ustunligi
        if ELEMENTS[attacker["element"]]["strong_against"] == defender["element"]:
            base_damage = int(base_damage * 1.3)
        
        # Critical hit
        if random.random() < 0.1:
            base_damage = int(base_damage * 1.5)
        
        return base_damage

# Bot komandalari
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Foydalanuvchini yaratish yoki olish
    user_data = db.get_user(user.id)
    if not user_data:
        db.create_user(user.id, user.first_name)
        user_data = db.get_user(user.id)
    
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    welcome_text = f"""
{texts['welcome'].format(name=user.first_name)}

Bu yerda siz:
• Anime personaj kartalarini to'plashingiz mumkin
• Epik janglarda qatnashishingiz mumkin  
• Qahramonlaringizni rivojlantirishingiz mumkin

{texts['menu']}
    """
    
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard(language))

async def get_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    # Foydalanuvchini tekshirish
    if not user_data:
        db.create_user(user.id, user.first_name)
        user_data = db.get_user(user.id)
    
    user_cards = db.get_user_cards(user.id)
    
    if len(user_cards) == 0:
        # Boshlang'ich kartalar berish
        random_chars = db.get_random_characters(3)
        for char in random_chars:
            db.add_user_card(user.id, char["id"])
        
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
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    user_cards = db.get_user_cards(user.id)
    
    if not user_cards:
        text = f"❌ {texts['need_3_cards']} '{texts['get_cards']}' tugmasi orqali boshlang'ich kartalarni oling!"
    else:
        text = f"🧳 **{texts['my_cards']}:**\n\n"
        for i, card in enumerate(user_cards, 1):
            element_emoji = {
                "Fire": "🔥", "Water": "💧", "Wind": "🌪️", 
                "Earth": "🌍", "Lightning": "⚡", "Light": "✨", "Dark": "🌑"
            }[card["element"]]
            
            rarity_emoji = {
                "Common": "⚪", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟡"
            }[card["rarity"]]
            
            text += f"""
{i}. {rarity_emoji} **{card['name']}** {element_emoji}
   ❤️ HP: {card['hp']} | ⚔️ Hujum: {card['attack']} 
   🛡️ Himoya: {card['defense']} | 🏃 Tezlik: {card['speed']}
────────────────
            """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    user_cards = db.get_user_cards(user.id)
    
    if len(user_cards) < 3:
        text = f"❌ {texts['need_3_cards']} '{texts['get_cards']}' orqali kartalarni oling!"
        await update.message.reply_text(text, reply_markup=get_main_keyboard(language))
        return
    
    # User jamoasi (birinchi 3 ta karta)
    user_team = user_cards[:3]
    
    # CPU jamoasini yaratish
    cpu_team = db.get_random_characters(3)
    
    # Jang natijasini hisoblash (soddalashtirilgan)
    user_power = sum(card["attack"] + card["defense"] for card in user_team)
    cpu_power = sum(card["attack"] + card["defense"] for card in cpu_team)
    
    win_chance = user_power / (user_power + cpu_power)
    
    if random.random() < win_chance:
        # G'alaba
        reward = random.randint(50, 100)
        db.update_balance(user.id, reward)
        db.update_user_stats(user.id, True)
        result_text = texts['victory'].format(reward=reward)
    else:
        # Mag'lubiyat
        reward = random.randint(10, 30)
        db.update_balance(user.id, reward)
        db.update_user_stats(user.id, False)
        result_text = texts['defeat'].format(reward=reward)
    
    battle_report = f"""
⚔️ **JANG NATIJASI**

🎯 **Sizning jamoangiz:**
{chr(10).join([f"• {card['name']} ({card['rarity']})" for card in user_team])}

🤖 **CPU jamoasi:**
{chr(10).join([f"• {card['name']} ({card['rarity']})" for card in cpu_team])}

{result_text}
    """
    
    await update.message.reply_text(battle_report, reply_markup=get_main_keyboard(language))

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    if not user_data:
        db.create_user(user.id, user.first_name)
        user_data = db.get_user(user.id)
    
    user_cards = db.get_user_cards(user.id)
    total_battles = user_data["wins"] + user_data["losses"]
    win_rate = (user_data["wins"] / total_battles * 100) if total_battles > 0 else 0
    
    text = f"""
{texts['player_profile']}

{texts['player']} {user.first_name}
{texts['balance_text']} {user_data['balance']} tanga

{texts['wins']} {user_data['wins']}
{texts['losses']} {user_data['losses']}
{texts['win_rate']} {win_rate:.1f}%

{texts['total_cards']} {len(user_cards)}
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def arena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    text = f"""
🏟️ **ARENA**

Xush kelibsiz, {user.first_name}!

**Mavjud rejimlar:**
⚔️ Tezkor jang - CPU bilan jang
🎯 Kunlik mashqlar - (Tez orada)
🏆 Reyting janglari - (Tez orada)

**Sizning statistikangiz:**
💰 Balans: {user_data['balance']} tanga
🎯 Gʻalabalar: {user_data['wins']}
💔 Magʻlubiyatlar: {user_data['losses']}

'{texts['start_battle']}' tugmasi orqali tezkor jangni boshlang!
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def clans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    
    text = f"""
🛡️ **KLANLAR**

Klanlarga qoʻshiling yoki oʻz klaningizni yarating!

**Klan imkoniyatlari:**
• Klan yaratish (1000 tanga)
• Mavjud klanga qoʻshilish  
• Klan janglarida qatnashish
• Klan bonuslarini olish

*Klan tizimi tez orada qoʻshiladi!*

Hozircha siz:
• Kartalarni to'plash 🌼
• Janglarga qatnashish ⚔️
• Koleksiyangizni yaxshilash 🧳
    """
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard(language))

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    text = f"""
{texts['shop']}

{texts['your_balance'].format(balance=user_data['balance'])}

**Mavjud toʻplamlar:**

{texts['starter_pack']}
• 3 ta tasodifiy karta
• Yangi boshlovchilar uchun ideal

{texts['premium_pack']}  
• 5 ta karta
• Yuqori sifatli kartalar
    """
    
    keyboard = [
        [InlineKeyboardButton(texts['starter_pack'], callback_data="shop_starter")],
        [InlineKeyboardButton(texts['premium_pack'], callback_data="shop_premium")],
        [InlineKeyboardButton(texts['back'], callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    text = f"""
📜 **ASOSIY MENYU**

**Oʻyin funksiyalari:**
🎮 Asosiy rejimlar
🎴 Karta kolleksiyasi  
⚔️ Jang tizimi
🛍️ Doʻkon

**Tez orada:**
🏆 Reyting janglari
👥 Klanlar
🎯 Kunlik vazifalar

**Qoʻllab-quvvatlash:**
❓ Yordam
🔧 Sozlamalar
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
    language = user_data["language"] if user_data else 'uz'
    texts = TEXTS[language]
    
    data = query.data
    
    if data.startswith("shop_"):
        if not user_data:
            db.create_user(user.id, user.first_name)
            user_data = db.get_user(user.id)
        
        if data == "shop_starter":
            cost = 100
            pack_type = "boshlang'ich"
            chars = db.get_random_characters(3)
        elif data == "shop_premium":
            cost = 500
            pack_type = "premium" 
            chars = db.get_random_characters(5)
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
            db.add_user_card(user.id, char["id"])
        
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
    language = user_data["language"] if user_data else 'uz'
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
    # Eski ma'lumotlar bazasini o'chirish
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑️ Eski ma'lumotlar bazasi o'chirildi")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Anime Battle Bot ishga tushdi...")
    print("🌐 Tillar: O'zbekcha, Русский, English")
    print("🎴 10 ta personaj mavjud")
    print("⚔️ Jang tizimi faol")
    
    # Botni ishga tushirish
    application.run_polling()

if __name__ == "__main__":
    main()