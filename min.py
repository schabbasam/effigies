
from direct.showbase.ShowBase import ShowBase
import sys

from camera import CameraController
from save_manager import SaveManager
from settings import Settings
from island import Island
from ui import UI
from interaction import Interactor
import colors

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.accept("escape", sys.exit)
        
        self.setBackgroundColor(colors.SKY)

        self.save_manager = SaveManager()
        self.settings = Settings(self.save_manager)
        self.camera_controller = CameraController(self, self.settings)
        self.island = Island(self)
        self.ui = UI(self)
        self.interactor = Interactor(self)


app = App()
app.run()

