# 🌀 Anime Battle Bot

## Loyiha haqida
**Anime Battle Bot** — bu Python va `python-telegram-bot` kutubxonasi yordamida ishlab chiqilgan aqlli anime jang o'yini botidir. Foydalanuvchilar o'z anime personajlari bilan **CPU** yoki **real foydalanuvchilar**ga qarshi jang qilib, **Anicoin**, **Battlecoin** va **Jeton** to'plashi mumkin.

## 📁 Loyiha tuzilmasi

```
.
├── main.py                 # Bot asosiy fayli va handler ro'yxati
├── config.py              # Konfiguratsiya va konstantalar
├── database.py            # Database class va operatsiyalar
├── models.py              # Data modellari (User, Character, Team, etc.)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (BOT_TOKEN)
├── data/
│   ├── characters.json    # 91 ta anime character ma'lumotlari
│   └── anime_battle.db    # SQLite database
├── handlers/              # Bot command va callback handlerlar
│   ├── __init__.py
│   ├── start.py          # /start command handler
│   ├── profile.py        # Profil boshqaruvi
│   ├── cards.py          # Karta olish va boshqarish
│   ├── menu.py           # Menyu navigatsiyasi
│   ├── arena.py          # Jang arena
│   └── admin.py          # Admin buyruqlari
└── utils/                 # Yordamchi funksiyalar
    ├── __init__.py
    ├── keyboards.py       # Telegram keyboard layoutlar
    ├── helpers.py         # Yordamchi funksiyalar
    ├── battle_logic.py    # Jang tizimi logikasi
    └── cpu_ai.py          # Aqlli CPU AI tizimi
```

## ✨ Asosiy xususiyatlar

### 👤 Foydalanuvchi tizimi
- ✅ Foydalanuvchi ro'yxatdan o'tish va profil tracking
- ✅ Ko'p valyuta tizimi: Anicoin, Battlecoin, Jeton, Keys
- ✅ Premium foydalanuvchi qo'llab-quvvatlash
- ✅ G'alaba/mag'lubiyat statistikasi

### 🎴 Character tizimi
- ✅ 91+ anime characterlar (Naruto, Dragon Ball, One Piece, va boshqalar)
- ✅ Rarity tizimi: Common, Rare, Epic, Legendary, Mythical
- ✅ Element tizimi: Fire, Water, Wind, Earth, Light, Dark, Lightning, Ice
- ✅ Character statistikasi: HP, ATK, DEF, SPD
- ✅ Level va experience tizimi

### ⚔️ Jang tizimi (YANGI!)
- ✅ **CPU bilan jang** - 4 qiyinlik darajasi:
  - 🟢 Oson - Yangi boshlovchilar uchun
  - 🟡 O'rta - Tajribali o'yinchilar uchun
  - 🔴 Qiyin - Mutaxassislar uchun
  - 🎯 Aqlli - AI pattern recognition bilan
- ✅ **Aqlli CPU AI tizimi**:
  - Player harakatlarini tahlil qiladi
  - Oldingi yurishlarga qarab strategiya tanlaydi
  - Element advantage exploitation
  - HP va Speed-based decision making
  - Counter-strategy system
- ✅ Turn-based jang mexanikasi
- ✅ Speed-based attack order
- ✅ Element advantage system
- ✅ Critical hits (15-25% chance)
- ✅ 3 harakatlar: Attack, Defend, Special
- ✅ Battle log va real-time yangilanishlar
- ✅ Mukofotlar va jazo tizimi

### 🎮 O'yin xususiyatlari
- ✅ Karta olish tizimi:
  - 🎫 Jeton orqali (24 soatda 1 marta)
  - 🛒 Anicoin bilan sotib olish
- ✅ **Komanda boshqaruvi** (3-5 character)
- ✅ **Klan tizimi**:
  - Klan yaratish va boshqarish
  - Klan banki (battlecoin)
  - Maksimal 5 a'zo (kengaytirilishi mumkin)
  - Parol himoyasi
- ✅ **Arena tizimi**:
  - CPU janglar
  - Real player janglar (UI tayyor)
  - Xona ochish/kirish (UI tayyor)
  - Turnirlar (UI tayyor)
  - Boss janglar (UI tayyor)
- ✅ Kunlik jeton claim tizimi (24 soat cooldown)
- ✅ Referral tizimi

### 👑 Admin funksiyalari
- ✅ Valyuta qo'shish/olib tashlash
- ✅ Premium status berish
- ✅ Foydalanuvchi ma'lumotlarini ko'rish
- ✅ Bot statistikasi
- ✅ Broadcast xabarlar (UI tayyor)

## 🎯 Asosiy menyular

### Asosiy tugmalar:
1. **🃏 Karta olish**
   - Jeton orqali karta olish (24 soat)
   - Anicoin orqali sotib olish

2. **📦 Mening kartalarim**
   - Barcha kartalarni ko'rish
   - Karta statistikalarini ko'rish
   - Navigation (oldingi/keyingi)

3. **⚙️ Menyu**
   - 👥 Komandam - Komanda boshqaruvi
   - 🛡️ Klan - Klan tizimi
   - 🛒 Magazin - Valyuta sotib olish
   - 🏆 Reyting - Top o'yinchilar
   - 🎯 Vazifalar - Kunlik vazifalar
   - 📢 Referal - Do'stlarni taklif qilish
   - ⚔️ Arena - Janglar va turnirlar

4. **👤 Profil**
   - Balanslar
   - Kartalar soni
   - Jang statistikasi
   - Referal kodi

## 💰 Valyuta tizimi

| Valyuta        | Tavsif                    | Qanday olinadi                     |
| -------------- | ------------------------- | ---------------------------------- |
| **Anicoin** 🪙 | Asosiy o'yin valyutasi    | Jang g'alabalari, vazifa, referal |
| **Battlecoin** | Premium valyuta           | Premium janglar, turnirlar         |
| **Jeton** 🎫   | Karta olish tokeni        | 24 soatda 1 ta                     |
| **Keys** 🔑    | Maxsus sandiqlar uchun    | Event va vazifalar                 |

## ⚔️ Jang mexanikasi

### Jang bosqichlari:
1. Jang turini tanlash (CPU/Real)
2. Qiyinlik darajasini tanlash (CPU uchun)
3. Komandani tanlash (3 yoki 5 character)
4. Jang boshlash
5. Har bir raundda harakat tanlash:
   - ⚔️ **Attack** - Oddiy hujum
   - 🛡️ **Defend** - Mudofaa (DEF +50%)
   - ✨ **Special** - Kuchli hujum (1.8x damage)
6. G'olib mukofot oladi, mag'lub valyuta yo'qotadi

### Element ustunliklari:
- 🔥 Fire > 💨 Wind
- 💨 Wind > 🌍 Earth
- 🌍 Earth > 💧 Water
- 💧 Water > 🔥 Fire
- ⚡ Light > 🌑 Dark
- 🌑 Dark > ⚡ Light

### Rarity multipliers:
- ⚪ Common: 1.0x
- 🔵 Rare: 1.3x
- 🟣 Epic: 1.7x
- 🟡 Legendary: 2.2x
- 🔴 Mythical: 3.0x

## 🧠 Aqlli CPU AI tizimi

CPU raqib foydalanuvchi harakatlarini o'rganadi va strategiyasini moslaydi:

- **Pattern Recognition**: Player qaysi harakatni ko'proq ishlatishini tahlil qiladi
- **Counter Strategy**: Playerning kamchiligidan foydalanadi
- **Element Awareness**: Element ustunligidan foydalanadi
- **HP Management**: O'z sog'ligini boshqaradi
- **Speed-based Decision**: Tezlikka qarab hujum yoki himoyani tanlaydi
- **Adaptive Difficulty**: Har bir qiyinlik darajasi o'ziga xos strategiyaga ega

## 🎮 Buyruqlar

### Foydalanuvchi buyruqlari:
- `/start` - Botni boshlash va ro'yxatdan o'tish
- Asosiy tugmalar: "Karta olish", "Mening kartalarim", "Profil", "Menyu"

### Admin buyruqlari (ADMIN_ID: 5371043130):
- `/admin` - Admin panel
- `/addcoins <user_id> <amount>` - Anicoin qo'shish
- `/addbattlecoins <user_id> <amount>` - Battlecoin qo'shish
- `/addjeton <user_id> <amount>` - Jeton qo'shish
- `/addkeys <user_id> <amount>` - Keys qo'shish
- `/setpremium <user_id>` - Premium berish
- `/userinfo <user_id>` - User ma'lumotlari
- `/stats` - Bot statistikasi

## 💾 Database

SQLite database quyidagi jadvallarni o'z ichiga oladi:
- `users` - Foydalanuvchi hisobi va valyuta
- `chars` - Character shablonlari
- `owned_chars` - User-owned characterlar va stats
- `teams` - Foydalanuvchi komandalari
- `clans` - Klan ma'lumotlari
- `clan_members` - Klan a'zolari
- `battles` - Jang yozuvlari

## 🚀 Ishga tushirish

Bot Replit muhitida avtomatik ishga tushadi:

1. Environment variable `.env` faylida:
   ```
   BOT_TOKEN=7995099850:AAFaan-VTbWJtuDKVLQoL4Yk4nLVCz7jxgU
   ```

2. Workflow avtomatik ishga tushadi:
   ```bash
   python main.py
   ```

3. Bot ishga tushganda:
   - ✅ Database yuklanadi/yaratiladi
   - ✅ 91 ta character data/characters.json dan yuklanadi
   - ✅ Telegram API ga ulanadi
   - ✅ Polling boshlanadi

## 📊 Bot holati

✅ **ISHLAYAPTI** - Bot faol va foydalanuvchilarning xabarlariga javob beryapti.

## 🔧 Texnologik stack

- **Til**: Python 3.11
- **Bot Framework**: python-telegram-bot 20.7
- **Database**: SQLite3
- **Muhit**: Replit
- **Config**: python-dotenv
- **AI**: Custom battle logic va CPU AI

## 📝 Oxirgi o'zgarishlar (2025-10-17)

### Qo'shilgan funksiyalar:
- ✅ To'liq jang tizimi (battle_logic.py)
- ✅ Aqlli CPU AI (cpu_ai.py)
- ✅ 4 qiyinlik darajasi (Easy, Medium, Hard, Smart)
- ✅ Pattern recognition tizimi
- ✅ Element advantage hisoblash
- ✅ Critical hit system
- ✅ Turn-based battle mechanics
- ✅ Real-time battle log
- ✅ Mukofot va jazo tizimi

### Tuzatilgan xatolar:
- ✅ Config.py - BOT_TOKEN loading
- ✅ characters.json - file nomi va data typo
- ✅ models.py - type annotations
- ✅ handlers/start.py - import paths
- ✅ handlers/profile.py - callback query handling
- ✅ database.py - db instance export

### Arxitektura:
- ✅ Modular kod tuzilmasi
- ✅ Ajratilgan logic (handlers, utils, models)
- ✅ Reusable components
- ✅ Clean code principles

## 👨‍💻 Muallif

**Bot Developer**: Replit AI Agent
**Platform**: Replit
**Versiya**: 1.0.0
**Sana**: 2025-10-17

---

## 📈 Kelgusi yangilanishlar

Keyingi versiyalarda qo'shiladi:
- 🚧 Real player matchmaking
- 🚧 Tournament tizimi
- 🚧 Boss battle mechanics
- 🚧 Ranking system
- 🚧 Daily quests
- 🚧 Card upgrade system
- 🚧 Card selling feature
- 🚧 Seasonal events

## 🎯 Xulosa

**Anime Battle Bot** — bu to'liq funksional, aqlli va interaktiv o'yin boti. Foydalanuvchilar anime characterlar bilan jang qilishlari, komanda boshqarishlari, klan yaratashlari va boshqa ko'plab funksiyalardan foydalanishlari mumkin!

Bot muvaffaqiyatli ishlayapti va foydalanishga tayyor! 🎮⚔️
