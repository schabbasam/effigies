# SaveManager reads and writes the user's settings and highscore.

import copy
import json
import sys
from pathlib import Path
from settings import Settings

class SaveManager:
    def __init__(self):
        if getattr(sys, "frozen", False):
            self.path = Path(sys.executable).resolve().parent / "user_data.json"
        else:
            self.path = Path(__file__).resolve().parent / "user_data.json"

        self._data = {}
        self.load()

    def load(self):
        if not self.path.exists():
            self._data = {
                "settings": copy.deepcopy(Settings.DEFAULT_SETTINGS),
                "highscore": 0
            }
            self.save()
            print("WARNING: no user_data.json found, generating a new file with defaults")
            return

        with self.path.open("r", encoding="utf-8") as file:
            self._data = json.load(file)

    def data(self):
        return self._data

    def save(self):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4, ensure_ascii=False)
