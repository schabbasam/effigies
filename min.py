
from direct.showbase.ShowBase import ShowBase
import sys

from camera import CameraController
from save_manager import SaveManager
from settings import Settings

class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.loadBox()
        
        self.accept("escape", sys.exit)

        self.save_manager = SaveManager()
        self.settings = Settings(self.save_manager)
        self.camera_controller = CameraController(self, self.settings)

    def loadBox(self):
        block = self.loader.loadModel("models/box")
        block.reparentTo(self.render)
        block.setScale(60, 60, 1)
        block.setPos(-29, -32, 0)

        self.camera.setPos(3, -3, 4)
        self.camera.lookAt(0, 0, 0.5)


app = App()
app.run()

