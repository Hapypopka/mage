# Конфигурация подземелий VMMO

import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.json")

# Порядок прохождения данженов (список)
DUNGEON_ORDER = [
    "dng:dSanctuary",      # Святилище Накрила (первый)
    "dng:dHellRuins",
    "dng:RestMonastery",
    "dng:HighDungeon",
    "dng:CitadelHolding",
    "dng:Underlight",
    "dng:way2Baron",
    "dng:Barony",
    "dng:ShadowGuard",
]

# Загружаем стартовый индекс из settings.json
def _load_start_index():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get('start_dungeon_index', 0)
        except Exception:
            pass
    return 0

START_DUNGEON_INDEX = _load_start_index()

# Список всех подземелий
DUNGEONS = {
    "dng:dSanctuary": {
        "name": "Sanctuary",
        "need_difficulty": False,  # Не нужно менять сложность
    },
    "dng:dHellRuins": {
        "name": "Hell Ruins",
        "need_difficulty": True,
        "difficulty_path": "dHellRuins",
    },
    "dng:RestMonastery": {
        "name": "Rest Monastery",
        "need_difficulty": True,
        "difficulty_path": "RestMonastery",
    },
    "dng:HighDungeon": {
        "name": "High Dungeon",
        "need_difficulty": True,
        "difficulty_path": "HighDungeon",
    },
    "dng:CitadelHolding": {
        "name": "Citadel Holding",
        "need_difficulty": True,
        "difficulty_path": "CitadelHolding",
    },
    "dng:Underlight": {
        "name": "Underlight",
        "need_difficulty": True,
        "difficulty_path": "Underlight",
    },
    "dng:way2Baron": {
        "name": "Way to Baron",
        "need_difficulty": False,  # Нельзя изменить сложность
    },
    "dng:Barony": {
        "name": "Barony",
        "need_difficulty": True,
        "difficulty_path": "Barony",
    },
    "dng:ShadowGuard": {
        "name": "Shadow Guard",
        "need_difficulty": True,
        "difficulty_path": "ShadowGuard",
    },
}

# Селектор для повышения сложности
DIFFICULTY_SELECTOR = "a.switch-level-left"
