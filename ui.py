# manages the user interface

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib, Vec4
from direct.gui.DirectGui import DirectFrame

import colors

class UI:
    def __init__(self, app):
        self.app = app
        self.crosshair = None
        
        self.color_frames = []
        self.selected_color = 0

        self.createColorBar()
        self.updateColorBar(0)

        self.createCrosshair()

    def createCrosshair(self):
        self.crosshair = OnscreenImage(
                image="assets/crosshair.png",
                pos=(0, 0, 0),
                scale=0.04
        )

        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        self.crosshair.setBin("fixed", 10)
        self.crosshair.setColor(1, 1, 1, 0.8)

    def createColorBar(self):
        count = len(colors.LIST)
        spacing = 0.2
        size = 0.065
        start_x = -(count - 1) * spacing / 2

        for i, color in enumerate(colors.LIST):
            frame = DirectFrame(
                frameColor=color[0],
                frameSize=(-size, size, -size, size),
                pos=(start_x + i * spacing, 0, -0.8),
                relief=1
            )

            self.color_frames.append(frame)

    def updateColorBar(self, selected):
        self.selected_color = selected

        for i, frame in enumerate(self.color_frames):
            frame["frameColor"] = colors.LIST[i][0]
            frame["frameSize"] = (
                -0.065, 0.065, -0.065, 0.065
            ) if i == selected else (
                -0.05, 0.05, -0.05, 0.05
            )
