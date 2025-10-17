from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class Character:
    id: int
    name: str
    element: str
    rarity: str
    base_hp: int
    base_atk: int
    base_def: int
    base_spd: int
    price: int
    image_url: Optional[str] = None
    skills: List[Dict] = None

    def __post_init__(self):
        if self.skills is None:
            self.skills = []

@dataclass
class OwnedCharacter:
    id: int
    user_id: int
    char_id: int
    level: int
    hp: int
    atk: int
    def_: int
    spd: int
    exp: int
    obtained_at: datetime
    source: str

@dataclass
class User:
    user_id: int
    username: str
    started_at: datetime
    premium: bool
    anicoin: int
    battlecoin: int
    jeton: int
    keys: int
    total_matches: int
    wins: int
    referral_code: str
    last_jeton_claim: Optional[datetime] = None
    clan_id: Optional[int] = None

@dataclass
class Team:
    id: int
    user_id: int
    name: str
    char_ids: List[int]
    is_active: bool

@dataclass
class Clan:
    id: int
    name: str
    owner_id: int
    password: str
    battlecoin_bank: int
    capacity: int
    created_at: datetime
    description: str

@dataclass
class Battle:
    match_id: str
    players: List[Dict]
    state: str
    current_turn: int
    turn_timeout: datetime
    log: List[Dict]
    created_at: datetime