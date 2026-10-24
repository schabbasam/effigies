# all settings are managed here

import copy

class Settings:

    # this needs to have every variable in the settings in user_data.json
    # otherwise, there will be an error
    DEFAULT_SETTINGS = {
                "speed": 2,
                "sensitivity": 80.0,
                "keybinds": {
                        "forward": "w",
                        "backward": "s",
                        "left": "a",
                        "right": "d",
                        "up": "space",
                        "down": "shift"
                    }
            }

    def __init__(self, save_manager):
        # using only one SaveManager across the game to prevent complications
        self.save_manager = save_manager

        # this is a reference, not a copy
        # it directly changes the SaveManager's data
        self._settings = self.save_manager.data()["settings"]

    def save(self):
        self.save_manager.save()

    def resetToDefault(self):
        # clears all values
        # simply replacing it would disconnect it from the
        # data provided by SaveManager
        self._settings.clear()

        # deepcopy is necessary to properly restore nested dictionaries
        # otherwise the defaults might accidentally be edited
        self._settings.update(copy.deepcopy(self.DEFAULT_SETTINGS))

    # --- all the setters and getters ---

    @property
    def sensitivity(self):
        return self._settings["sensitivity"]

    @sensitivity.setter
    def sensitivity(self, value):
        self._settings["sensitivity"] = value
    
    @property
    def keybinds(self):
        return self._settings["keybinds"]

    @keybinds.setter
    def keybinds(self, value):
        self._settings["keybinds"]

    @property
    def speed(self):
        return self._settings["speed"]

    @speed.setter
    def speed(self, value):
        self._settings["speed"]
