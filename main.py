import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN, ADMIN_ID
from database import db
from handlers import (
    start, show_profile, handle_profile_callbacks,
    show_card_acquisition, show_my_cards, handle_card_callbacks,
    claim_jeton, show_buy_cards, show_menu, handle_menu_callbacks,
    show_arena, handle_arena_callbacks, admin_panel, handle_admin_commands
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_main_buttons(update, context):
    """Asosiy tugmalarni boshqarish"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == "Karta olish":
        await show_card_acquisition(update, context)
    elif text == "Mening kartalarim":
        await show_my_cards(update, context)
    elif text == "Profil":
        await show_profile(update, context)
    elif text == "Menyu":
        await show_menu(update, context)
    else:
        await update.message.reply_text("Iltimos, quyidagi tugmalardan foydalaning:")

async def handle_message(update, context):
    """Oddiy xabarlarni boshqarish"""
    user_id = update.effective_user.id
    
    # Agar xabar matn bo'lsa va command bo'lmasa
    if update.message.text and not update.message.text.startswith('/'):
        await handle_main_buttons(update, context)

def main():
    """Botni ishga tushirish"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! Iltimos, .env faylida TOKEN ni o'rnating.")
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("addcoins", handle_admin_commands))
    application.add_handler(CommandHandler("addbattlecoins", handle_admin_commands))
    application.add_handler(CommandHandler("addjeton", handle_admin_commands))
    application.add_handler(CommandHandler("addkeys", handle_admin_commands))
    application.add_handler(CommandHandler("setpremium", handle_admin_commands))
    application.add_handler(CommandHandler("userinfo", handle_admin_commands))
    application.add_handler(CommandHandler("stats", handle_admin_commands))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(handle_profile_callbacks, pattern="^(settings|back_to_profile|back_to_main)$"))
    application.add_handler(CallbackQueryHandler(handle_card_callbacks, pattern="^(card_|buy_|back_to_card|claim_jeton)"))
    application.add_handler(CallbackQueryHandler(handle_menu_callbacks, pattern="^(team_|clan_|shop_|arena_|leaderboard|quests|referral|menu_back)$"))
    application.add_handler(CallbackQueryHandler(handle_arena_callbacks, pattern="^(battle_|create_|join_|tournament|boss_|arena_back)$"))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Botni ishga tushirish
    print("🤖 Anime Battle Bot ishga tushdi...")
    print(f"👑 Admin ID: {ADMIN_ID}")
    application.run_polling()

if __name__ == '__main__':
    main()