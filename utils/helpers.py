from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import ELEMENT_ADVANTAGES, RARITY_MULTIPLIERS

def format_time_delta(delta: timedelta) -> str:
    """Vaqt farqini formatlash"""
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return f"{hours} soat {minutes} daqiqa"

def calculate_element_advantage(attacker_element: str, defender_element: str) -> float:
    """Element advantage multiplier hisoblash"""
    if ELEMENT_ADVANTAGES.get(attacker_element) == defender_element:
        return 1.3  # 30% damage bonus
    elif ELEMENT_ADVANTAGES.get(defender_element) == attacker_element:
        return 0.7  # 30% damage reduction
    return 1.0

def calculate_damage(attacker_atk: int, defender_def: int, 
                    element_multiplier: float = 1.0, 
                    skill_multiplier: float = 1.0,
                    critical: bool = False) -> int:
    """Damage hisoblash"""
    base_damage = max(1, int((attacker_atk * skill_multiplier) - (defender_def * 0.5)))
    damage = int(base_damage * element_multiplier)
    
    if critical:
        damage = int(damage * 1.5)
    
    return max(1, damage)

def get_rarity_multiplier(rarity: str) -> float:
    """Rarity multiplier olish"""
    return RARITY_MULTIPLIERS.get(rarity, 1.0)

def get_element_emoji(element: str) -> str:
    """Element uchun emoji"""
    emojis = {
        "fire": "🔥", "water": "💧", "earth": "🌍", 
        "wind": "💨", "light": "⚡", "dark": "🌑"
    }
    return emojis.get(element, "❓")

def get_rarity_emoji(rarity: str) -> str:
    """Rarity uchun emoji"""
    emojis = {
        "common": "⚪", "rare": "🔵", "epic": "🟣",
        "legendary": "🟡", "mythical": "🔴"
    }
    return emojis.get(rarity, "⚪")

def format_character_stats(character, owned_char=None):
    """Karta statistikalarini formatlash"""
    if owned_char:
        hp = owned_char.hp
        atk = owned_char.atk
        def_ = owned_char.def_
        spd = owned_char.spd
        level = owned_char.level
    else:
        hp = character.base_hp
        atk = character.base_atk
        def_ = character.base_def
        spd = character.base_spd
        level = 1
    
    element_emoji = get_element_emoji(character.element)
    rarity_emoji = get_rarity_emoji(character.rarity)
    
    return f"""
🎴 **{character.name}**

{element_emoji} Element: {character.element}
{rarity_emoji} Rarity: {character.rarity}
📊 Level: {level}

⚔️ **Statistikalar:**
❤️ HP: {hp}
🗡️ ATK: {atk}
🛡️ DEF: {def_} 
⚡ SPD: {spd}
"""