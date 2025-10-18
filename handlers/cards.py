# handlers/cards.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from utils.keyboards import (
    get_card_acquisition_keyboard, get_card_detail_keyboard,
    get_pagination_keyboard
)
from utils.helpers import format_character_stats, format_time_delta
from database import db

async def show_card_acquisition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎴 **Karta olish**

Quyidagi usullardan biri bilan yangi kartalar olishingiz mumkin:

🎫 **Jeton olish** - Har 24 soatda 1 marta bepul karta olish
🛒 **Karta sotib olish** - Anicoin bilan kartalar sotib olish

💡 **Maslahat:** Har kuni jeton olishni unutmang!
"""
    
    if update.message:
        await update.message.reply_text(text, reply_markup=get_card_acquisition_keyboard())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=get_card_acquisition_keyboard())

async def claim_jeton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        await query.edit_message_text("❌ Xatolik: Foydalanuvchi topilmadi")
        return
    
    # 24 soatlik cooldown tekshirish
    if user.last_jeton_claim and datetime.now() - user.last_jeton_claim < timedelta(hours=24):
        next_claim = user.last_jeton_claim + timedelta(hours=24)
        time_left = next_claim - datetime.now()
        
        await query.edit_message_text(
            f"⏳ **Jeton olish uchun {format_time_delta(time_left)} qoldi!**\n\n"
            f"🔁 Keyingi marta: {next_claim.strftime('%Y-%m-%d %H:%M')}",
            parse_mode='Markdown'
        )
        return
    
    # Jeton berish
    db.update_user_currency(user_id, jeton=1)
    
    # Last claim vaqtini yangilash
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET last_jeton_claim = ? WHERE user_id = ?', 
        (datetime.now(), user_id)
    )
    conn.commit()
    conn.close()
    
    # Yangi user ma'lumotlari
    user = db.get_user(user_id)
    
    await query.edit_message_text(
        f"✅ **+1 Jeton qo'shildi!**\n\n"
        f"🎫 Jetonlar soni: `{user.jeton}`\n\n"
        f"Endi yangi kartalar olishingiz mumkin! 🎴",
        parse_mode='Markdown'
    )

async def show_buy_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    
    # Barcha kartalarni olish
    all_characters = db.get_all_characters()
    page = 0
    characters_per_page = 5
    
    await show_cards_page(query, context, all_characters, page, characters_per_page)

async def show_cards_page(query, context, all_characters: list, page: int, per_page: int):
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_characters = all_characters[start_idx:end_idx]
    
    total_pages = (len(all_characters) + per_page - 1) // per_page
    
    text = f"🛒 **Karta sotib olish**\n\n"
    text += f"📄 Sahifa {page + 1}/{total_pages}\n\n"
    text += "Quyidagi kartalardan birini tanlang:\n\n"
    
    keyboard_buttons = []
    
    for char in page_characters:
        char_text = f"🎴 {char.name} - {char.price} 🪙"
        keyboard_buttons.append([
            InlineKeyboardButton(char_text, callback_data=f"buy_char_{char.id}")
        ])
    
    # Pagination tugmalari
    pagination_row = []
    if page > 0:
        pagination_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"buy_page_{page-1}"))
    
    pagination_row.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="buy_info"))
    
    if page < total_pages - 1:
        pagination_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"buy_page_{page+1}"))
    
    if pagination_row:
        keyboard_buttons.append(pagination_row)
    
    keyboard_buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_card_acquisition")])
    
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def show_my_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_cards = db.get_user_characters(user_id)
    
    if not user_cards:
        if update.message:
            await update.message.reply_text(
                "📭 **Sizda hali kartalar mavjud emas!**\n\n"
                "«Karta olish» bo'limiga o'tib, birinchi kartangizni oling! 🎴",
                parse_mode='Markdown'
            )
        else:
            await update.callback_query.edit_message_text(
                "📭 **Sizda hali kartalar mavjud emas!**\n\n"
                "«Karta olish» bo'limiga o'tib, birinchi kartangizni oling! 🎴",
                parse_mode='Markdown'
            )
        return
    
    # Birinchi kartani ko'rsatish
    first_card = user_cards[0]
    char_template = db.get_character(first_card.char_id)
    
    if not char_template:
        if update.message:
            await update.message.reply_text("❌ Xatolik: Karta ma'lumotlari topilmadi")
        else:
            await update.callback_query.edit_message_text("❌ Xatolik: Karta ma'lumotlari topilmadi")
        return
    
    card_text = format_character_stats(char_template, first_card)
    card_text += f"\n📄 1/{len(user_cards)}"
    
    keyboard = get_card_detail_keyboard(first_card.id, 0, len(user_cards))
    
    if update.message:
        await update.message.reply_text(card_text, reply_markup=keyboard, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(card_text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_card_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    if data == "back_to_card_acquisition":
        await show_card_acquisition(update, context)
    
    elif data == "buy_cards":
        await show_buy_cards(update, context)
    
    elif data.startswith("buy_page_"):
        page = int(data.split("_")[2])
        all_characters = db.get_all_characters()
        await show_cards_page(query, context, all_characters, page, 5)
    
    elif data.startswith("buy_char_"):
        char_id = int(data.split("_")[2])
        await purchase_character(query, context, char_id)
    
    elif data.startswith("card_prev_") or data.startswith("card_next_"):
        current_index = int(data.split("_")[2])
        user_cards = db.get_user_characters(user_id)
        
        if data.startswith("card_prev_"):
            new_index = max(0, current_index - 1)
        else:
            new_index = min(len(user_cards) - 1, current_index + 1)
        
        card = user_cards[new_index]
        char_template = db.get_character(card.char_id)
        
        if char_template:
            card_text = format_character_stats(char_template, card)
            card_text += f"\n📄 {new_index + 1}/{len(user_cards)}"
            
            keyboard = get_card_detail_keyboard(card.id, new_index, len(user_cards))
            await query.edit_message_text(card_text, reply_markup=keyboard, parse_mode='Markdown')
    
    elif data == "back_to_cards":
        await show_my_cards(update, context)

async def purchase_character(query, context, char_id: int):
    user_id = query.from_user.id
    user = db.get_user(user_id)
    character = db.get_character(char_id)
    
    if not character:
        await query.edit_message_text("❌ Xatolik: Karta topilmadi")
        return
    
    if user.anicoin < character.price:
        await query.edit_message_text(
            f"❌ **Yetarli Anicoin mavjud emas!**\n\n"
            f"Karta narxi: {character.price} 🪙\n"
            f"Sizning balansingiz: {user.anicoin} 🪙\n\n"
            f"Qo'shimcha Anicoin olish uchun magazinga tashrif buyuring!",
            parse_mode='Markdown'
        )
        return
    
    # Karta sotib olish
    db.update_user_currency(user_id, anicoin=-character.price)
    success = db.add_character_to_user(user_id, char_id, "purchase")
    
    if success:
        await query.edit_message_text(
            f"✅ **{character.name} kartasi sotib olindi!**\n\n"
            f"💳 Xarajat: {character.price} 🪙\n"
            f"💰 Qolgan balans: {user.anicoin - character.price} 🪙\n\n"
            f"Kartangizni «Mening kartalarim» bo'limida ko'rishingiz mumkin! 🎴",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text("❌ Xatolik: Karta sotib olishda xatolik yuz berdi")