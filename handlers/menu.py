from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.keyboards import get_menu_keyboard, get_arena_keyboard, get_clan_keyboard, get_shop_keyboard
from database import db

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
🧭 **Menyu**

Quyidagi bo'limlardan birini tanlang:

👥 **Komandam** - Jangovar komandalaringizni boshqaring
🛡️ **Klan** - Klan tizimi
🛒 **Magazin** - Valyutalar sotib olish
🏆 **Reyting** - Eng yaxshi o'yinchilar
🎯 **Vazifalar** - Kunlik va haftalik vazifalar
📢 **Referal** - Do'stlaringizni taklif qiling
⚔️ **Arena** - Janglar va turnirlar
"""
    
    await update.message.reply_text(menu_text, reply_markup=get_menu_keyboard(), parse_mode='Markdown')

async def handle_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "menu_back":
        await show_menu(update, context)
    
    elif data == "team_management":
        await show_team_management(query, context)
    
    elif data == "clan_menu":
        await show_clan_menu(query, context)
    
    elif data == "shop_menu":
        await show_shop_menu(query, context)
    
    elif data == "arena_menu":
        await show_arena_menu(query, context)
    
    elif data == "leaderboard":
        await show_leaderboard(query, context)
    
    elif data == "quests":
        await show_quests(query, context)
    
    elif data == "referral":
        await show_referral(query, context)

async def show_team_management(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    teams = db.get_user_teams(user_id)
    
    text = "👥 **Komanda boshqaruvi**\n\n"
    
    if not teams:
        text += "📭 Sizda hali hech qanday komanda saqlanmagan.\n\n"
    else:
        text += "💾 **Saqangan komandalaringiz:**\n"
        for team in teams:
            status = "✅ Faol" if team.is_active else "❌ Nofaol"
            text += f"• {team.name} - {status}\n"
        text += "\n"
    
    text += "Komanda yaratish yoki mavjud komandani tahrirlash uchun quyidagi tugmalardan foydalaning."
    
    keyboard_buttons = []
    
    for team in teams:
        keyboard_buttons.append([
            InlineKeyboardButton(f"👥 {team.name}", callback_data=f"team_view_{team.id}")
        ])
    
    keyboard_buttons.extend([
        [InlineKeyboardButton("➕ Yangi komanda", callback_data="team_create")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])
    
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_clan_menu(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    user_clan = db.get_user_clan(user_id)
    
    text = "🛡️ **Klan tizimi**\n\n"
    
    if user_clan:
        text += f"🎯 **Sizning klaningiz:** {user_clan.name}\n"
        text += f"👑 Egasi: {user_clan.owner_id}\n"
        text += f"👥 A'zolar: {user_clan.capacity} ta\n"
        text += f"🏦 Bank: {user_clan.battlecoin_bank} battlecoin\n\n"
    else:
        text += "📭 Siz hali hech qanday klanga a'zo emassiz.\n\n"
    
    text += "Klan yaratish yoki mavjud klanga qo'shilish uchun quyidagi tugmalardan foydalaning."
    
    await query.edit_message_text(text, reply_markup=get_clan_keyboard(), parse_mode='Markdown')

async def show_shop_menu(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    text = f"""
🛒 **Magazin**

💰 **Joriy balansingiz:**
• Anicoin: `{user.anicoin}` 🪙
• Battlecoin: `{user.battlecoin}` ⚔️
• Kalitlar: `{user.keys}` 🔑

💳 **Sotib olish uchun valyutani tanlang:**

🪙 **Anicoin** - Asosiy o'yin valyutasi
⚔️ **Battlecoin** - Premium janglar valyutasi  
🔑 **Kalitlar** - Maxsus sandiqlarni ochish

💬 *Valyuta sotib olish uchun admin (@) bilan bog'laning*
"""
    
    await query.edit_message_text(text, reply_markup=get_shop_keyboard(), parse_mode='Markdown')

async def show_arena_menu(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
⚔️ **Arena**

Jang maydoniga xush kelibsiz! Quyidagi jang turlaridan birini tanlang:

🤖 **CPU bilan jang** - Bot bilan mashq jangi
👤 **Real jang** - Haqiqiy o'yinchi bilan jang
👥 **Xona ochish** - Do'stlaringiz bilan xususiy jang
🚪 **Xonaga kirish** - Mavjud xonaga qo'shilish
🏆 **Turnir** - Ko'p o'yinchi turnirlari
🐉 **Boss jangi** - Kuchli boss bilan jang

💥 Janglar orqali tajriba va resurslar toping!
"""
    
    await query.edit_message_text(text, reply_markup=get_arena_keyboard(), parse_mode='Markdown')

async def show_leaderboard(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🏆 **Reyting**

🚧 *Reyting tizimi hozircha ishlab chiqilmoqda. Tez orada qo'shiladi!*

📊 Kelgusi yangilanishlarda quyidagi reytinglar bo'ladi:
• Top 10 gʻalaba
• Mavsumiy reyting
• Top donatorlar
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_quests(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎯 **Vazifalar**

🚧 *Vazifalar tizimi hozircha ishlab chiqilmoqda. Tez orada qo'shiladi!*

📝 Kelgusi yangilanishlarda quyidagi vazifalar bo'ladi:
• Kunlik vazifalar
• Haftalik vazifalar
• Maxsus tadbir vazifalari
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_referral(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    text = f"""
📢 **Referal tizimi**

🎁 Do'stlaringizni taklif qiling va mukofotlar oling!

🔗 **Sizning referal havolangiz:**
`https://t.me/your_bot_username?start={user.referral_code}`

📋 **Sizning referal kodingiz:**
`{user.referral_code}`

🏆 **Mukofotlar:**
• Har bir taklif qilingan do'st uchun: 50 Anicoin 🪙
• Do'stingizning birinchi g'alabasi uchun: 100 Anicoin 🪙

💡 Do'stlaringiz havola orqali botga kirib, /start bosishlari kifoya!
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Havolani ulashish", switch_inline_query=f"Botga qo'shiling! {user.referral_code}")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')