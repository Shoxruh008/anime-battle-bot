# Anime Battle Bot

## Overview
This is a Telegram bot for an anime battle card game where users can collect anime characters, create teams, and battle against other players. The bot is built with Python using the `python-telegram-bot` library and SQLite database.

## Project Structure

```
.
├── main.py                 # Main bot entry point and handler registration
├── config.py              # Configuration settings and constants
├── database.py            # Database class and operations
├── models.py              # Data models (User, Character, Team, Clan, etc.)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (BOT_TOKEN)
├── data/
│   ├── characters.json    # Character data (91 anime characters)
│   └── anime_battle.db    # SQLite database
├── handlers/              # Bot command and callback handlers
│   ├── __init__.py
│   ├── start.py          # /start command
│   ├── profile.py        # Profile management
│   ├── cards.py          # Card acquisition and management
│   ├── menu.py           # Menu navigation
│   ├── arena.py          # Battle arena
│   └── admin.py          # Admin commands
└── utils/                 # Utility functions
    ├── __init__.py
    ├── keyboards.py       # Telegram keyboard layouts
    └── helpers.py         # Helper functions
```

## Features

### User Management
- User registration and profile tracking
- Multiple currency system: Anicoin, Battlecoin, Jeton, Keys
- Premium user support
- Win/loss statistics

### Character System
- 91+ anime characters from popular series (Naruto, Dragon Ball, One Piece, etc.)
- Rarity system: Common, Rare, Epic, Legendary, Mythical
- Element system: Fire, Water, Wind, Earth, Light, Dark, Lightning, Ice
- Character stats: HP, ATK, DEF, SPD
- Level and experience system

### Game Features
- Card acquisition system
- Team building (up to 3 characters)
- Clan system with banking
- Battle arena with element advantages
- Daily jeton claim system
- Referral system

### Admin Features
- Add/remove currencies
- Set premium status
- View user information
- Bot statistics

## Setup and Configuration

### Environment Variables
The bot requires a `BOT_TOKEN` environment variable set in the `.env` file:
```
BOT_TOKEN=your_telegram_bot_token_here
```

### Admin Configuration
The admin user ID is configured in `config.py`:
```python
ADMIN_ID = 5371043130
```

## Database Schema

The SQLite database includes the following tables:
- `users` - User accounts and currency
- `chars` - Character templates
- `owned_chars` - User-owned characters with stats
- `teams` - User teams
- `clans` - Clan information
- `clan_members` - Clan membership
- `battles` - Battle records

## How to Run

The bot is configured to run automatically via the "Telegram Bot" workflow. The workflow executes:
```bash
python main.py
```

When the bot starts:
1. Database is initialized/loaded
2. Character data is loaded from `data/characters.json`
3. Bot connects to Telegram API
4. Polling begins for user messages

## Recent Changes (October 17, 2025)

### Import Setup
- Installed Python 3.11 and dependencies
- Fixed `config.py` to correctly load `BOT_TOKEN` from environment variable
- Fixed import paths in handlers to use `utils.keyboards` instead of `keyboards`
- Centralized database instance creation in `database.py`

### Data Fixes
- Renamed `character.json` to `characters.json` for consistency
- Fixed typo in character #83 (Hinata Hyuga): `base_de` → `base_def`

### Type Fixes
- Fixed type annotation in `models.py`: Changed `skills: List[Dict] = None` to `skills: Optional[List[Dict]] = None`

### Project Configuration
- Created `.gitignore` for Python project
- Configured workflow for console output
- Created project documentation

## Bot Status
✅ **Currently Running** - The bot is active and responding to Telegram messages.

## Game Mechanics

### Currency System
- **Anicoin** 🪙: Primary currency for buying cards (starting: 100)
- **Battlecoin**: Earned from battles (starting: 0)
- **Jeton** 🎫: Can be claimed daily (starting: 1)
- **Keys**: Used for special features (starting: 0)

### Element Advantages
- Fire beats Wind
- Wind beats Earth
- Earth beats Water
- Water beats Fire
- Light beats Dark
- Dark beats Light

### Rarity Multipliers
- Common: 1.0x
- Rare: 1.3x
- Epic: 1.7x
- Legendary: 2.2x
- Mythical: 3.0x

## Commands

### User Commands
- `/start` - Start the bot and register
- Main buttons: "Karta olish", "Mening kartalarim", "Profil", "Menyu"

### Admin Commands (Admin ID only)
- `/admin` - Admin panel
- `/addcoins` - Add Anicoin to user
- `/addbattlecoins` - Add Battlecoin to user
- `/addjeton` - Add Jeton to user
- `/addkeys` - Add Keys to user
- `/setpremium` - Set premium status
- `/userinfo` - Get user information
- `/stats` - Bot statistics

## Technology Stack
- **Language**: Python 3.11
- **Bot Framework**: python-telegram-bot 20.7
- **Database**: SQLite3
- **Environment**: Replit
- **Config**: python-dotenv for environment variables
