# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard
from database import db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # User mavjudligini tekshirish
    existing_user = db.get_user(user_id)
    if not existing_user:
        db.create_user(user_id, user.username or user.first_name)
        existing_user = db.get_user(user_id)
    
    if not existing_user:
        await update.message.reply_text("Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")
        return
    
    welcome_text = f"""
🎌 **Anime Jang** botiga xush kelibsiz, {user.first_name}!

Bu yerda siz anime personajlari bilan strategik janglar qilishingiz mumkin.

🏁 **Boshlash uchun quyidagi tugmalardan foydalaning:**

• **Karta olish** - Yangi kartalar olish
• **Mening kartalarim** - Kartalaringizni boshqarish  
• **Profil** - Shaxsiy hisobingiz
• **Menyu** - Qo'shimcha funksiyalar

💰 **Boshlang'ich balansingiz:**
• {existing_user.anicoin} Anicoin 🪙
• {existing_user.jeton} Jeton 🎫

Jang qilish va g'alaba qozonish orqali ko'proq resurslar toping!
"""
    
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')