from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Karta olish"), KeyboardButton("Mening kartalarim")],
        [KeyboardButton("Menyu"), KeyboardButton("Profil")]
    ], resize_keyboard=True)

def get_profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔧 Sozlamalar", callback_data="settings")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
    ])

def get_card_acquisition_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎫 Jeton olish (24 soat)", callback_data="claim_jeton")],
        [InlineKeyboardButton("🛒 Karta sotib olish", callback_data="buy_cards")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
    ])

def get_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Komandam", callback_data="team_management")],
        [InlineKeyboardButton("🛡️ Klan", callback_data="clan_menu")],
        [InlineKeyboardButton("🛒 Magazin", callback_data="shop_menu")],
        [InlineKeyboardButton("🏆 Reyting", callback_data="leaderboard")],
        [InlineKeyboardButton("🎯 Vazifalar", callback_data="quests")],
        [InlineKeyboardButton("📢 Referal", callback_data="referral")],
        [InlineKeyboardButton("⚔️ Arena", callback_data="arena_menu")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
    ])

def get_card_detail_keyboard(card_id: int, current_index: int, total_cards: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏪", callback_data=f"card_prev_{current_index}"),
            InlineKeyboardButton("⚔️", callback_data=f"card_battle_{card_id}"),
            InlineKeyboardButton("⏩", callback_data=f"card_next_{current_index}")
        ],
        [
            InlineKeyboardButton("⬆️ Kuchaytirish", callback_data=f"card_upgrade_{card_id}"),
            InlineKeyboardButton("💰 Sotish", callback_data=f"card_sell_{card_id}")
        ],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_cards")]
    ])

def get_arena_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 CPU bilan jang", callback_data="battle_cpu")],
        [InlineKeyboardButton("👤 Real jang", callback_data="battle_real")],
        [InlineKeyboardButton("👥 Xona ochish", callback_data="create_room")],
        [InlineKeyboardButton("🚪 Xonaga kirish", callback_data="join_room")],
        [InlineKeyboardButton("🏆 Turnir", callback_data="tournament")],
        [InlineKeyboardButton("🐉 Boss jangi", callback_data="boss_battle")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])

def get_clan_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛡️ Klan yaratish", callback_data="clan_create")],
        [InlineKeyboardButton("🚪 Klan qo'shilish", callback_data="clan_join")],
        [InlineKeyboardButton("👥 Mening klanim", callback_data="clan_my")],
        [InlineKeyboardButton("🏦 Klan banki", callback_data="clan_bank")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])

def get_shop_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Anicoin sotib olish", callback_data="shop_anicoin")],
        [InlineKeyboardButton("⚔️ Battlecoin sotib olish", callback_data="shop_battlecoin")],
        [InlineKeyboardButton("🔑 Kalitlar sotib olish", callback_data="shop_keys")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back")]
    ])

def get_pagination_keyboard(page: int, total_pages: int, prefix: str):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"{prefix}_page_{page-1}"))
    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"{prefix}_page_{page+1}"))
    
    return InlineKeyboardButton([buttons]) if buttons else None