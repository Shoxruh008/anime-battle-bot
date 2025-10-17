import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from models import User, Character, OwnedCharacter, Team, Clan

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_db()
        self.load_characters()
    
    def get_connection(self):
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                started_at TIMESTAMP,
                premium BOOLEAN DEFAULT FALSE,
                anicoin INTEGER DEFAULT 100,
                battlecoin INTEGER DEFAULT 0,
                jeton INTEGER DEFAULT 1,
                keys INTEGER DEFAULT 0,
                total_matches INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                referral_code TEXT,
                last_jeton_claim TIMESTAMP,
                clan_id INTEGER
            )
        ''')
        
        # Characters template jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chars (
                id INTEGER PRIMARY KEY,
                name TEXT,
                element TEXT,
                rarity TEXT,
                base_hp INTEGER,
                base_atk INTEGER,
                base_def INTEGER,
                base_spd INTEGER,
                price_anicoin INTEGER,
                image_url TEXT,
                skills TEXT
            )
        ''')
        
        # Owned characters jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS owned_chars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT,
                char_id INTEGER,
                level INTEGER DEFAULT 1,
                hp INTEGER,
                atk INTEGER,
                def INTEGER,
                spd INTEGER,
                exp INTEGER DEFAULT 0,
                obtained_at TIMESTAMP,
                source TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (char_id) REFERENCES chars (id)
            )
        ''')
        
        # Teams jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT,
                name TEXT,
                char_ids TEXT,
                is_active BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Clans jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                owner_id BIGINT,
                password TEXT,
                battlecoin_bank INTEGER DEFAULT 0,
                capacity INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT DEFAULT ''
            )
        ''')
        
        # Clan members jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clan_members (
                clan_id INTEGER,
                user_id BIGINT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                role TEXT DEFAULT 'member',
                PRIMARY KEY (clan_id, user_id),
                FOREIGN KEY (clan_id) REFERENCES clans (id),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Battles jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battles (
                match_id TEXT PRIMARY KEY,
                players TEXT,
                state TEXT,
                current_turn INTEGER DEFAULT 0,
                turn_timeout TIMESTAMP,
                log TEXT,
                created_at TIMESTAMP,
                finished_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_characters(self):
        """Characters.json dan ma'lumotlarni yuklash"""
        try:
            with open('data/characters.json', 'r', encoding='utf-8') as f:
                characters_data = json.load(f)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            for char_data in characters_data:
                skills_json = json.dumps(char_data.get('skills', []))
                
                cursor.execute('''
                    INSERT OR REPLACE INTO chars 
                    (id, name, element, rarity, base_hp, base_atk, base_def, base_spd, price_anicoin, image_url, skills)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    char_data['id'], char_data['name'], char_data['element'],
                    char_data['rarity'], char_data['base_hp'], char_data['base_atk'],
                    char_data['base_def'], char_data['base_spd'], char_data['price_anicoin'],
                    char_data['image_url'], skills_json
                ))
            
            conn.commit()
            conn.close()
            print("✅ Characters ma'lumotlari yuklandi")
        except Exception as e:
            print(f"❌ Characters yuklashda xatolik: {e}")
    
    # USER METHODS
    def get_user(self, user_id: int) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                user_id=row[0], username=row[1], started_at=datetime.fromisoformat(row[2]),
                premium=bool(row[3]), anicoin=row[4], battlecoin=row[5], jeton=row[6],
                keys=row[7], total_matches=row[8], wins=row[9], referral_code=row[10],
                last_jeton_claim=datetime.fromisoformat(row[11]) if row[11] else None,
                clan_id=row[12]
            )
        return None
    
    def create_user(self, user_id: int, username: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        referral_code = f"REF{user_id}{datetime.now().strftime('%H%M%S')}"
        
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, started_at, referral_code)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, datetime.now(), referral_code))
        
        conn.commit()
        conn.close()
    
    def update_user_currency(self, user_id: int, **currencies):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        for currency, value in currencies.items():
            if value != 0:
                updates.append(f"{currency} = {currency} + ?")
                params.append(value)
        
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            params.append(user_id)
            cursor.execute(query, params)
        
        conn.commit()
        conn.close()
    
    def update_user_stats(self, user_id: int, win: bool = False):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET total_matches = total_matches + 1,
                wins = wins + ?
            WHERE user_id = ?
        ''', (1 if win else 0, user_id))
        
        conn.commit()
        conn.close()
    
    # CHARACTER METHODS
    def get_character(self, char_id: int) -> Optional[Character]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM chars WHERE id = ?', (char_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            skills = json.loads(row[10]) if row[10] else []
            return Character(
                id=row[0], name=row[1], element=row[2], rarity=row[3],
                base_hp=row[4], base_atk=row[5], base_def=row[6], base_spd=row[7],
                price_anicoin=row[8], image_url=row[9], skills=skills
            )
        return None
    
    def get_all_characters(self) -> List[Character]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM chars')
        rows = cursor.fetchall()
        conn.close()
        
        characters = []
        for row in rows:
            skills = json.loads(row[10]) if row[10] else []
            characters.append(Character(
                id=row[0], name=row[1], element=row[2], rarity=row[3],
                base_hp=row[4], base_atk=row[5], base_def=row[6], base_spd=row[7],
                price_anicoin=row[8], image_url=row[9], skills=skills
            ))
        
        return characters
    
    def get_user_characters(self, user_id: int) -> List[OwnedCharacter]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM owned_chars WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        characters = []
        for row in rows:
            characters.append(OwnedCharacter(
                id=row[0], user_id=row[1], char_id=row[2], level=row[3],
                hp=row[4], atk=row[5], def_=row[6], spd=row[7], exp=row[8],
                obtained_at=datetime.fromisoformat(row[9]), source=row[10]
            ))
        
        return characters
    
    def add_character_to_user(self, user_id: int, char_id: int, source: str = "purchase"):
        char_template = self.get_character(char_id)
        if not char_template:
            return False
        
        # Calculate stats based on level and rarity
        rarity_multiplier = {
            "common": 1.0, "rare": 1.2, "epic": 1.5, 
            "legendary": 2.0, "mythical": 2.5
        }.get(char_template.rarity, 1.0)
        
        hp = int(char_template.base_hp * rarity_multiplier)
        atk = int(char_template.base_atk * rarity_multiplier)
        def_ = int(char_template.base_def * rarity_multiplier)
        spd = int(char_template.base_spd * rarity_multiplier)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO owned_chars 
            (user_id, char_id, level, hp, atk, def, spd, exp, obtained_at, source)
            VALUES (?, ?, 1, ?, ?, ?, ?, 0, ?, ?)
        ''', (user_id, char_id, hp, atk, def_, spd, datetime.now(), source))
        
        conn.commit()
        conn.close()
        return True
    
    # TEAM METHODS
    def get_user_teams(self, user_id: int) -> List[Team]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM teams WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        teams = []
        for row in rows:
            char_ids = json.loads(row[3]) if row[3] else []
            teams.append(Team(
                id=row[0], user_id=row[1], name=row[2], 
                char_ids=char_ids, is_active=bool(row[4])
            ))
        
        return teams
    
    def create_team(self, user_id: int, name: str, char_ids: List[int]):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        char_ids_json = json.dumps(char_ids)
        
        cursor.execute('''
            INSERT INTO teams (user_id, name, char_ids, is_active)
            VALUES (?, ?, ?, ?)
        ''', (user_id, name, char_ids_json, False))
        
        conn.commit()
        conn.close()
    
    # CLAN METHODS
    def create_clan(self, name: str, owner_id: int, password: str, description: str = ""):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clans (name, owner_id, password, description)
            VALUES (?, ?, ?, ?)
        ''', (name, owner_id, password, description))
        
        clan_id = cursor.lastrowid
        
        # Add owner to clan members
        cursor.execute('''
            INSERT INTO clan_members (clan_id, user_id, role)
            VALUES (?, ?, 'owner')
        ''', (clan_id, owner_id))
        
        conn.commit()
        conn.close()
        return clan_id
    
    def get_clan(self, clan_id: int) -> Optional[Clan]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clans WHERE id = ?', (clan_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Clan(
                id=row[0], name=row[1], owner_id=row[2], password=row[3],
                battlecoin_bank=row[4], capacity=row[5], 
                created_at=datetime.fromisoformat(row[6]), description=row[7]
            )
        return None
    
    def get_user_clan(self, user_id: int) -> Optional[Clan]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.* FROM clans c
            JOIN clan_members cm ON c.id = cm.clan_id
            WHERE cm.user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Clan(
                id=row[0], name=row[1], owner_id=row[2], password=row[3],
                battlecoin_bank=row[4], capacity=row[5],
                created_at=datetime.fromisoformat(row[6]), description=row[7]
            )
        return None