# Конфигурация подземелий VMMO

import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.json")

# Порядок прохождения данженов (список)
DUNGEON_ORDER = [
    "dng:dSanctuary",      # Святилище Накрила (первый)
    "dng:dHellRuins",
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
        "need_difficulty": False,
    },
    "dng:HighDungeon": {
        "name": "High Dungeon",
        "need_difficulty": False,
    },
    "dng:CitadelHolding": {
        "name": "Citadel Holding",
        "need_difficulty": False,
    },
    "dng:Underlight": {
        "name": "Underlight",
        "need_difficulty": False,
    },
    "dng:way2Baron": {
        "name": "Way to Baron",
        "need_difficulty": False,
    },
    "dng:Barony": {
        "name": "Barony",
        "need_difficulty": False,
    },
    "dng:ShadowGuard": {
        "name": "Shadow Guard",
        "need_difficulty": False,
    },
}

# Селектор для повышения сложности
DIFFICULTY_SELECTOR = "a.switch-level-left"
