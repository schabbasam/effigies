# SaveManager reads and writes the user's settings and highscore.

import json
import sys
from pathlib import Path


class SaveManager:
    def __init__(self):
        # In a packaged build, keep saves beside the executable so they remain
        # writable and survive updates. In development, use the project folder.
        if getattr(sys, "frozen", False):
            self.path = Path(sys.executable).resolve().parent / "user_data.json"
        else:
            self.path = Path(__file__).resolve().parent / "user_data.json"

        self._data = {}
        self.load()

    def load(self):
        with self.path.open("r", encoding="utf-8") as file:
            self._data = json.load(file)

    def data(self):
        return self._data

    def save(self):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4, ensure_ascii=False)
