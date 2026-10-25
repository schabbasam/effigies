# SaveManager reads and writes the user_data.json

import json
from pathlib import Path

class SaveManager:
    def __init__(self):
        self.path = Path("user_data.json")

        # this is a "copy" of the original
        # it shouldn't be accessed directly, hence the _
        self._data = {}
        
        # load the file already when SaveManager is called
        self.load()

    def load(self):
        with self.path.open("r", encoding="utf-8") as file:
            self._data = json.load(file)

    def data(self):
        return self._data

    def save(self):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4, ensure_ascii=False)

