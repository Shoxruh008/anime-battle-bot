# handlers/admin.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import ADMIN_ID
from database import db

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel ko'rsatish"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Sizga ruxsat yo'q!")
        return
    
    text = """
👑 **Admin Panel**

Quyidagi buyruqlar mavjud:

/addcoins <user_id> <amount> - Anicoin qo'shish
/addbattlecoins <user_id> <amount> - Battlecoin qo'shish  
/addjeton <user_id> <amount> - Jeton qo'shish
/addkeys <user_id> <amount> - Kalitlar qo'shish

/setpremium <user_id> - Premium berish
/removepremium <user_id> - Premium olib tashlash

/broadcast <xabar> - Hammaga xabar yuborish
/stats - Bot statistikasi

/userinfo <user_id> - User ma'lumotlari
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_admin_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin buyruqlarini boshqarish"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Sizga ruxsat yo'q!")
        return
    
    command = update.message.text.split()[0]
    args = context.args
    
    if command == "/addcoins" and len(args) >= 2:
        target_user_id = int(args[0])
        amount = int(args[1])
        
        db.update_user_currency(target_user_id, anicoin=amount)
        await update.message.reply_text(f"✅ {target_user_id} ga {amount} Anicoin qo'shildi")
    
    elif command == "/addbattlecoins" and len(args) >= 2:
        target_user_id = int(args[0])
        amount = int(args[1])
        
        db.update_user_currency(target_user_id, battlecoin=amount)
        await update.message.reply_text(f"✅ {target_user_id} ga {amount} Battlecoin qo'shildi")
    
    elif command == "/addjeton" and len(args) >= 2:
        target_user_id = int(args[0])
        amount = int(args[1])
        
        db.update_user_currency(target_user_id, jeton=amount)
        await update.message.reply_text(f"✅ {target_user_id} ga {amount} Jeton qo'shildi")
    
    elif command == "/addkeys" and len(args) >= 2:
        target_user_id = int(args[0])
        amount = int(args[1])
        
        db.update_user_currency(target_user_id, keys=amount)
        await update.message.reply_text(f"✅ {target_user_id} ga {amount} Kalit qo'shildi")
    
    elif command == "/setpremium" and len(args) >= 1:
        target_user_id = int(args[0])
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET premium = TRUE WHERE user_id = ?', (target_user_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ {target_user_id} ga premium berildi")
    
    elif command == "/userinfo" and len(args) >= 1:
        target_user_id = int(args[0])
        user = db.get_user(target_user_id)
        
        if user:
            user_cards = db.get_user_characters(target_user_id)
            text = f"""
👤 **User Ma'lumotlari**

🆔 ID: `{user.user_id}`
🏷️ Ism: {user.username}
👑 Premium: {'✅' if user.premium else '❌'}
📅 Ro'yxatdan o'tgan: {user.started_at}

💰 Balanslar:
• Anicoin: {user.anicoin} 🪙
• Battlecoin: {user.battlecoin} ⚔️  
• Jeton: {user.jeton} 🎫
• Kalitlar: {user.keys} 🔑

📊 Statistika:
• Janglar: {user.total_matches}
• G'alabalar: {user.wins}
• G'alaba %: {(user.wins/user.total_matches*100) if user.total_matches > 0 else 0:.1f}%

🎴 Kartalar: {len(user_cards)} ta
"""
            await update.message.reply_text(text, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ User topilmadi")
    
    elif command == "/stats":
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM owned_chars')
        total_cards = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(total_matches) FROM users')
        total_matches = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(wins) FROM users')
        total_wins = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(anicoin) FROM users')
        total_anicoin = cursor.fetchone()[0] or 0
        
        conn.close()
        
        text = f"""
📊 **Bot Statistikasi**

👥 Jami foydalanuvchilar: {total_users}
🎴 Jami kartalar: {total_cards}
⚔️ Jami janglar: {total_matches}
🏆 Jami g'alabalar: {total_wins}
🪙 Jami Anicoin: {total_anicoin}

📈 O'rtacha jang/user: {total_matches/total_users if total_users > 0 else 0:.1f}
📊 O'rtacha g'alaba %: {(total_wins/total_matches*100) if total_matches > 0 else 0:.1f}%
"""
        await update.message.reply_text(text, parse_mode='Markdown')