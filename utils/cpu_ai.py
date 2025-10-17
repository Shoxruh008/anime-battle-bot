import random
from typing import List, Dict

class CPUAI:
    """Aqlli CPU tizimi"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.move_history = []
        self.player_patterns = {
            "attack": 0,
            "defend": 0,
            "special": 0
        }
    
    def decide_action(self, cpu_char: Dict, player_char: Dict) -> str:
        """CPU harakatini aniqlash"""
        
        # Qiyinlik darajasiga qarab
        if self.difficulty == "easy":
            return self._easy_logic(cpu_char, player_char)
        elif self.difficulty == "medium":
            return self._medium_logic(cpu_char, player_char)
        elif self.difficulty == "hard":
            return self._hard_logic(cpu_char, player_char)
        elif self.difficulty == "smart":
            return self._smart_logic(cpu_char, player_char)
        else:
            return random.choice(["attack", "defend", "special"])
    
    def record_player_move(self, move: str):
        """Player harakatini yozib qo'yish"""
        self.move_history.append(move)
        self.player_patterns[move] = self.player_patterns.get(move, 0) + 1
    
    def _easy_logic(self, cpu_char: Dict, player_char: Dict) -> str:
        """Oson - asosan random + ba'zi mantiq"""
        # 70% attack, 20% defend, 10% special
        rand = random.random()
        
        # Agar HP kam bo'lsa, mudofaa qilish
        if cpu_char['hp'] < cpu_char['hp'] * 0.3:
            if rand < 0.5:
                return "defend"
        
        if rand < 0.7:
            return "attack"
        elif rand < 0.9:
            return "defend"
        else:
            return "special"
    
    def _medium_logic(self, cpu_char: Dict, player_char: Dict) -> str:
        """O'rta - element advantage va HP balance"""
        cpu_hp_ratio = cpu_char['hp'] / (cpu_char['hp'] + 100)
        player_hp_ratio = player_char['hp'] / (player_char['hp'] + 100)
        
        # Agar CPU HP kam bo'lsa
        if cpu_hp_ratio < 0.3:
            return "defend"
        
        # Agar player HP kam bo'lsa - aggressive
        if player_hp_ratio < 0.4:
            return "special" if random.random() < 0.6 else "attack"
        
        # Element advantage bor bo'lsa - attack
        if self._has_element_advantage(cpu_char['element'], player_char['element']):
            return "attack" if random.random() < 0.7 else "special"
        
        # Default - balanced
        return random.choice(["attack", "attack", "defend", "special"])
    
    def _hard_logic(self, cpu_char: Dict, player_char: Dict) -> str:
        """Qiyin - complex strategy"""
        cpu_hp_ratio = cpu_char['hp'] / (cpu_char['hp'] + 100)
        player_hp_ratio = player_char['hp'] / (player_char['hp'] + 100)
        
        # Aggresive agar player HP kam
        if player_hp_ratio < 0.35:
            return "special" if random.random() < 0.7 else "attack"
        
        # Defensive agar CPU HP kam
        if cpu_hp_ratio < 0.4:
            return "defend" if random.random() < 0.8 else "attack"
        
        # Element advantage strategiyasi
        has_advantage = self._has_element_advantage(cpu_char['element'], player_char['element'])
        
        if has_advantage:
            # Attack yoki special - advantage exploitation
            return "special" if random.random() < 0.5 else "attack"
        else:
            # Balanced play
            if cpu_hp_ratio > 0.7:
                # Salomatlik yaxshi - aggressive
                return random.choice(["attack", "special", "attack"])
            else:
                # Ehtiyotkorlik
                return random.choice(["attack", "defend", "defend"])
    
    def _smart_logic(self, cpu_char: Dict, player_char: Dict) -> str:
        """Aqlli - player patternlarni analiz qilish"""
        cpu_hp_ratio = cpu_char['hp'] / (cpu_char['hp'] + 100)
        player_hp_ratio = player_char['hp'] / (player_char['hp'] + 100)
        
        # Player pattern analizi
        most_used_move = self._predict_player_move()
        
        # Counter strategy
        if most_used_move == "attack":
            # Player ko'p hujum qilsa - mudofaa yoki counter-attack
            if cpu_hp_ratio < 0.4:
                return "defend"
            else:
                return "special" if random.random() < 0.6 else "attack"
        
        elif most_used_move == "defend":
            # Player ko'p himoya qilsa - aggressive
            return "special" if random.random() < 0.7 else "attack"
        
        elif most_used_move == "special":
            # Player special ishlatsa - timing va HP management
            if cpu_hp_ratio > 0.6:
                return "attack"
            else:
                return "defend"
        
        # Situational decision
        if player_hp_ratio < 0.3:
            # Finish them!
            return "special"
        
        if cpu_hp_ratio < 0.3:
            # Survive
            return "defend" if random.random() < 0.7 else "attack"
        
        # Element advantage exploitation
        if self._has_element_advantage(cpu_char['element'], player_char['element']):
            return random.choice(["attack", "special", "attack"])
        
        # Speed-based strategy
        if cpu_char['spd'] > player_char['spd']:
            # Tezlik ustunligi - aggressive
            return random.choice(["attack", "special", "attack", "attack"])
        else:
            # Sekin - defensive va strategic
            return random.choice(["attack", "defend", "special"])
    
    def _predict_player_move(self) -> str:
        """Player keyingi harakatini bashorat qilish"""
        if not self.player_patterns:
            return "attack"
        
        total_moves = sum(self.player_patterns.values())
        if total_moves == 0:
            return "attack"
        
        # Eng ko'p ishlatiladigan harakat
        most_common = max(self.player_patterns, key=self.player_patterns.get)
        return most_common
    
    def _has_element_advantage(self, attacker_element: str, defender_element: str) -> bool:
        """Element ustunligi bormi"""
        advantages = {
            "fire": "wind",
            "wind": "earth",
            "earth": "water",
            "water": "fire",
            "light": "dark",
            "dark": "light",
            "lightning": "water",
            "ice": "earth"
        }
        
        return advantages.get(attacker_element.lower()) == defender_element.lower()
    
    def reset(self):
        """AI holatini reset qilish"""
        self.move_history = []
        self.player_patterns = {
            "attack": 0,
            "defend": 0,
            "special": 0
        }
