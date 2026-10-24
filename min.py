
from direct.showbase.ShowBase import ShowBase
import sys

from camera import CameraController
from save_manager import SaveManager
from settings import Settings
from island import Island

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.accept("escape", sys.exit)

        self.save_manager = SaveManager()
        self.settings = Settings(self.save_manager)
        self.camera_controller = CameraController(self, self.settings)
        self.island = Island(self)


app = App()
app.run()

