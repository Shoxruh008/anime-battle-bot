import random
from typing import List, Dict, Tuple
from utils.helpers import calculate_damage, calculate_element_advantage, get_rarity_multiplier
from models import OwnedCharacter, Character

class BattleState:
    """Jang holatini saqlash"""
    def __init__(self, player1_id: int, player2_id: int, player1_team: List, player2_team: List):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_team = player1_team
        self.player2_team = player2_team
        self.current_turn = random.choice([1, 2])
        self.round_number = 1
        self.battle_log = []
        self.player1_action = None
        self.player2_action = None
        
    def get_active_character(self, player: int):
        """Faol personajni olish"""
        team = self.player1_team if player == 1 else self.player2_team
        for char in team:
            if char['hp'] > 0:
                return char
        return None
    
    def is_team_defeated(self, player: int) -> bool:
        """Komanda mag'lubmi tekshirish"""
        team = self.player1_team if player == 1 else self.player2_team
        return all(char['hp'] <= 0 for char in team)
    
    def apply_damage(self, target_player: int, damage: int):
        """Damage qo'llash"""
        char = self.get_active_character(target_player)
        if char:
            char['hp'] = max(0, char['hp'] - damage)
            self.battle_log.append(f"💥 {char['name']} ga {damage} damage yedi! (HP: {char['hp']})")
    
    def switch_character(self, player: int):
        """Keyingi personajga o'tish"""
        team = self.player1_team if player == 1 else self.player2_team
        current_char = self.get_active_character(player)
        
        if current_char and current_char['hp'] <= 0:
            for i, char in enumerate(team):
                if char['hp'] > 0:
                    self.battle_log.append(f"🔄 {char['name']} maydonga kirdi!")
                    return True
        return False

class Battle:
    """Jang tizimi"""
    
    @staticmethod
    def execute_turn(state: BattleState, p1_action: str, p2_action: str) -> Dict:
        """Bir raundni bajarish"""
        p1_char = state.get_active_character(1)
        p2_char = state.get_active_character(2)
        
        if not p1_char or not p2_char:
            return {"error": "Invalid characters"}
        
        # Speed tekshirish - kim birinchi hujum qiladi
        p1_speed = p1_char['spd']
        p2_speed = p2_char['spd']
        
        if p1_speed > p2_speed:
            first, second = (1, p1_action, p1_char), (2, p2_action, p2_char)
        elif p2_speed > p1_speed:
            first, second = (2, p2_action, p2_char), (1, p1_action, p1_char)
        else:
            # Teng tezlik - random
            if random.choice([True, False]):
                first, second = (1, p1_action, p1_char), (2, p2_action, p2_char)
            else:
                first, second = (2, p2_action, p2_char), (1, p1_action, p1_char)
        
        # Birinchi hujum
        Battle._execute_action(state, first[0], first[1], first[2], 
                              2 if first[0] == 1 else 1)
        
        # Ikkinchi hujum (agar tirik bo'lsa)
        if not state.is_team_defeated(1) and not state.is_team_defeated(2):
            Battle._execute_action(state, second[0], second[1], second[2],
                                  1 if second[0] == 2 else 2)
        
        # Round tugadi
        state.round_number += 1
        
        return {
            "log": state.battle_log.copy(),
            "p1_team": state.player1_team,
            "p2_team": state.player2_team,
            "round": state.round_number,
            "winner": Battle.check_winner(state)
        }
    
    @staticmethod
    def _execute_action(state: BattleState, attacker: int, action: str, 
                       attacker_char: Dict, defender: int):
        """Harakatni bajarish"""
        defender_char = state.get_active_character(defender)
        
        if not defender_char:
            return
        
        if action == "attack":
            # Oddiy hujum
            element_mult = calculate_element_advantage(
                attacker_char['element'], defender_char['element']
            )
            
            # Critical chance
            critical = random.random() < 0.15
            
            damage = calculate_damage(
                attacker_char['atk'],
                defender_char['def'],
                element_mult,
                1.0,
                critical
            )
            
            state.apply_damage(defender, damage)
            
            crit_text = " 💥 CRITICAL!" if critical else ""
            state.battle_log.append(
                f"⚔️ {attacker_char['name']} hujum qildi!{crit_text}"
            )
        
        elif action == "defend":
            # Mudofaa
            attacker_char['def_boost'] = 1.5
            state.battle_log.append(
                f"🛡️ {attacker_char['name']} mudofaa holatiga o'tdi!"
            )
        
        elif action == "special":
            # Maxsus hujum - ko'proq damage, lekin kamroq ehtimol
            element_mult = calculate_element_advantage(
                attacker_char['element'], defender_char['element']
            )
            
            skill_mult = 1.8
            critical = random.random() < 0.25
            
            damage = calculate_damage(
                attacker_char['atk'],
                defender_char['def'],
                element_mult,
                skill_mult,
                critical
            )
            
            state.apply_damage(defender, damage)
            
            state.battle_log.append(
                f"✨ {attacker_char['name']} maxsus hujum qildi!"
            )
        
        # Character o'lganmi tekshirish
        if defender_char['hp'] <= 0:
            state.battle_log.append(
                f"💀 {defender_char['name']} yiqildi!"
            )
            state.switch_character(defender)
    
    @staticmethod
    def check_winner(state: BattleState) -> int:
        """G'olibni tekshirish"""
        if state.is_team_defeated(1):
            return 2
        elif state.is_team_defeated(2):
            return 1
        return 0
    
    @staticmethod
    def calculate_rewards(winner: int, loser: int, difficulty: str = "medium") -> Dict:
        """Mukofotlarni hisoblash"""
        rewards = {
            "winner_anicoin": 0,
            "winner_battlecoin": 0,
            "loser_anicoin": 0
        }
        
        # Difficulty bo'yicha mukofotlar
        multipliers = {
            "easy": 0.8,
            "medium": 1.0,
            "hard": 1.3,
            "smart": 1.5
        }
        
        mult = multipliers.get(difficulty, 1.0)
        
        rewards["winner_anicoin"] = int(100 * mult)
        rewards["winner_battlecoin"] = int(10 * mult)
        rewards["loser_anicoin"] = int(-30 * mult)
        
        return rewards
    
    @staticmethod
    def prepare_team(characters: List[OwnedCharacter], char_templates: Dict[int, Character]) -> List[Dict]:
        """Komandani tayyorlash"""
        team = []
        for char in characters:
            template = char_templates.get(char.char_id)
            if template:
                team.append({
                    'id': char.id,
                    'char_id': char.char_id,
                    'name': template.name,
                    'hp': char.hp,
                    'atk': char.atk,
                    'def': char.def_,
                    'spd': char.spd,
                    'element': template.element,
                    'level': char.level,
                    'def_boost': 1.0
                })
        return team

def create_cpu_team(difficulty: str, all_characters: List[Character]) -> List[Dict]:
    """CPU uchun komanda yaratish"""
    # Difficulty bo'yicha rarity tanlash
    rarity_pool = {
        "easy": ["common", "rare"],
        "medium": ["rare", "epic"],
        "hard": ["epic", "legendary"],
        "smart": ["legendary", "mythical"]
    }
    
    allowed_rarities = rarity_pool.get(difficulty, ["rare", "epic"])
    
    # Ruxsat etilgan kartalarni tanlash
    filtered_chars = [c for c in all_characters if c.rarity.lower() in allowed_rarities]
    
    if len(filtered_chars) < 3:
        filtered_chars = all_characters
    
    # 3 ta random karta tanlash
    selected = random.sample(filtered_chars, min(3, len(filtered_chars)))
    
    cpu_team = []
    for char in selected:
        mult = get_rarity_multiplier(char.rarity.lower())
        cpu_team.append({
            'id': -1,
            'char_id': char.id,
            'name': f"CPU {char.name}",
            'hp': int(char.base_hp * mult),
            'atk': int(char.base_atk * mult),
            'def': int(char.base_def * mult),
            'spd': int(char.base_spd * mult),
            'element': char.element,
            'level': 1,
            'def_boost': 1.0
        })
    
    return cpu_team