# handlers/profile.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.keyboards import get_profile_keyboard
from database import db

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ Xatolik: Foydalanuvchi topilmadi")
        return
    
    # Kartalar sonini hisoblash
    user_cards = db.get_user_characters(user_id)
    total_cards = len(user_cards)
    
    # Faol jang kartalari (level > 0)
    battle_cards = len([c for c in user_cards if c.level > 0])
    
    premium_status = "✅ Aktiv" if user.premium else "❌ Noaktiv"
    win_rate = (user.wins / user.total_matches * 100) if user.total_matches > 0 else 0
    
    profile_text = f"""
👤 **Profil**

🏷️ **Ism:** {user.username or "Noma'lum"}
🆔 **ID:** `{user.user_id}`
👑 **Premium:** {premium_status}
📅 **Start bosgan sana:** {user.started_at.strftime('%Y-%m-%d %H:%M')}

💰 **Balanslar:**
• Anicoin: `{user.anicoin}` 🪙
• Jeton: `{user.jeton}` 🎫
• Battlecoin: `{user.battlecoin}` ⚔️
• Kalitlar: `{user.keys}` 🔑

🎴 **Kartalar:**
• Jami kartalar: `{total_cards}`
• Jang kartalari: `{battle_cards}`

📊 **Statistika:**
• Jami janglar: `{user.total_matches}`
• Gʻalabalar: `{user.wins}`
• Gʻalaba foizi: `{win_rate:.1f}%`

📢 **Referal kodingiz:** `{user.referral_code}`
"""
    
    await update.message.reply_text(
        profile_text, 
        reply_markup=get_profile_keyboard(), 
        parse_mode='Markdown'
    )

async def handle_profile_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "settings":
        await show_settings(query, context)
    elif data == "back_to_main":
        await query.edit_message_text("🏠 Asosiy menyuga qaytdingiz")
    elif data == "back_to_profile":
        await show_profile(update, context)

async def show_settings(query, context: ContextTypes.DEFAULT_TYPE):
    settings_text = """
🔧 **Sozlamalar**

Bu yerda bot sozlamalarini o'zgartirishingiz mumkin.

🚧 *Hozircha sozlamalar mavjud emas. Tez orada qo'shiladi!*
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_profile")]
    ])
    
    await query.edit_message_text(settings_text, reply_markup=keyboard, parse_mode='Markdown')