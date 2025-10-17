from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import db

async def show_arena(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_arena_menu(update.callback_query, context)

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
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 CPU bilan jang", callback_data="battle_cpu")],
        [InlineKeyboardButton("👤 Real jang", callback_data="battle_real")],
        [InlineKeyboardButton("👥 Xona ochish", callback_data="create_room")],
        [InlineKeyboardButton("🚪 Xonaga kirish", callback_data="join_room")],
        [InlineKeyboardButton("🏆 Turnir", callback_data="tournament")],
        [InlineKeyboardButton("🐉 Boss jangi", callback_data="boss_battle")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_arena_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "battle_cpu":
        await start_cpu_battle(query, context)
    
    elif data == "battle_real":
        await start_real_battle(query, context)
    
    elif data == "create_room":
        await create_battle_room(query, context)
    
    elif data == "join_room":
        await join_battle_room(query, context)
    
    elif data == "tournament":
        await show_tournament(query, context)
    
    elif data == "boss_battle":
        await start_boss_battle(query, context)
    
    elif data == "arena_back":
        await show_arena_menu(query, context)

async def start_cpu_battle(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🤖 **CPU bilan jang**

Qiyinlik darajasini tanlang:

🟢 **Oson** - Yangi boshlovchilar uchun
🟡 **O'rta** - Tajribali o'yinchilar uchun  
🔴 **Qiyin** - Mutaxassislar uchun
🎯 **Aqlli** - AI bilan jang (tajriba talab qilinadi)

💡 Har bir daraja uchun mukofotlar farq qiladi!
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Oson", callback_data="cpu_easy"),
            InlineKeyboardButton("🟡 O'rta", callback_data="cpu_medium")
        ],
        [
            InlineKeyboardButton("🔴 Qiyin", callback_data="cpu_hard"),
            InlineKeyboardButton("🎯 Aqlli", callback_data="cpu_smart")
        ],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def start_real_battle(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
👤 **Real jang**

Haqiqiy o'yinchi bilan jang boshlash uchun qidiruv boshlandi...

🔍 **Qidiruv davom etmoqda...**
⏳ Taxminiy kutish vaqti: 10-30 soniya

📊 **Matchmaking parametrlari:**
• Skill darajangizga mos o'yinchi
• Xuddi shu region
• Teng jang statistikasi

🕹️ Jang boshlanganda sizga xabar beramiz!
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def create_battle_room(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
👥 **Xona ochish**

Xususiy jang xonasini yaratish:

📝 **Xona parametrlari:**
• 🎯 Maksimal o'yinchilar: 2
• ⏰ Vaqt cheklovi: 30 soniya
• 🔒 Parol: Ixtiyoriy

💡 Xona yaratilganda, sizga maxsus kod beriladi. Do'stlaringiz shu kod orqali qo'shilishi mumkin.
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Xona yaratish", callback_data="room_create_confirm")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def join_battle_room(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🚪 **Xonaga kirish**

Mavjud jang xonasiga qo'shilish uchun xona kodini kiriting:

📋 **Qo'shilish uchun:**
1. Do'stingizdan xona kodini oling
2. Kodni shu yerga yuboring
3. Jang avtomatik boshlanadi

💬 Xona kodini yuborish uchun shunchaki matn sifatida yuboring.
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_tournament(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🏆 **Turnirlar**

Hozirgi mavsumdagi turnirlar:

📅 **Faol turnirlar:**
• 🥇 Oylik Gran-pri (1-31)
• 🥈 Haftalik Challenger (10-17)
• 🥉 Kunlik Rapid (Har kuni)

📊 **Yaqinlashayotgan turnirlar:**
• Legend Cup - 5 kun qoldi
• Spring Championship - 12 kun qoldi

💎 Har bir turnir uchun alohida mukofotlar!
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Mavsum statistikasi", callback_data="tournament_stats")],
        [InlineKeyboardButton("🎯 Turnirga qo'shilish", callback_data="tournament_join")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def start_boss_battle(query, context: ContextTypes.DEFAULT_TYPE):
    text = """
🐉 **Boss jangi**

Kuchli bosslar bilan jang qiling va noyob mukofotlar yuting!

🎯 **Mavjud bosslar:**

🔥 **Flame Dragon** (Level 10)
• ❤️ HP: 5000 | 🗡️ ATK: 150
• 🎯 Zaiflik: Water 💧
• 🏆 Mukofot: 500 Anicoin + Rare karta

❄️ **Ice Titan** (Level 20) 
• ❤️ HP: 8000 | 🗡️ ATK: 200
• 🎯 Zaiflik: Fire 🔥
• 🏆 Mukofot: 1000 Anicoin + Epic karta

⚡ **Thunder Emperor** (Level 30)
• ❤️ HP: 12000 | 🗡️ ATK: 250  
• 🎯 Zaiflik: Earth 🌍
• 🏆 Mukofot: 2000 Anicoin + Legendary karta
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Flame Dragon", callback_data="boss_flame")],
        [InlineKeyboardButton("❄️ Ice Titan", callback_data="boss_ice")],
        [InlineKeyboardButton("⚡ Thunder Emperor", callback_data="boss_thunder")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="arena_back")]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')