# manages the user interface

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

class UI:
    def __init__(self, app):
        self.app = app
        self.crosshair = None

        self.createCrosshair()

    def createCrosshair(self):
        self.crosshair = OnscreenImage(
                image="assets/crosshair.png",
                pos=(0, 0, 0),
                scale=0.04
        )

        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        self.crosshair.setBin("fixed", 10)
