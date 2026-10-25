
# initializes and starts the game

from direct.showbase.ShowBase import ShowBase
import sys

from shader import Shader
from camera import CameraController
from save_manager import SaveManager
from settings import Settings
from island import Island
from ui import UI
from interaction import Interactor
from game_manager import GameManager

import colors


class App(ShowBase):
    def __init__(self):
        super().__init__()

        # close the game when the player presses Escape
        self.accept("escape", sys.exit)

        # set the background color
        self.setBackgroundColor(colors.SKY)

        # initialize settings and save data
        self.save_manager = SaveManager()
        self.settings = Settings(self.save_manager)

        # initialize the camera and game world
        self.camera_controller = CameraController(self, self.settings)
        self.island = Island(self)

        # initialize the user interface and player interactions
        self.ui = UI(self)
        self.interactor = Interactor(self, self.island)

        # initialize visual effects
        self.shader = Shader(self)

        # initialize the game logic and start the first round
        self.game_manager = GameManager(self)


def startGame():
    # create the application and initialize all game systems
    app = App()

    # start Panda3D's main loop
    # this runs until the application is closed
    app.run()

