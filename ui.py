# manages the user interface

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib, Vec4
from direct.gui.DirectGui import DirectFrame
from direct.gui.OnscreenText import OnscreenText

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
        self.createGameInfo()

    def createCrosshair(self):
        self.crosshair = OnscreenImage(
                image="assets/crosshair.png",
                pos=(0, 0, 0),
                scale=0.04
        )

        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
        self.crosshair.setBin("fixed", 10)
        self.crosshair.setColor(1, 1, 1, 0.8)

        # display the saved highscore in the top-left corner
        self.highscore_text = OnscreenText(
            text="Highscore: 0",
            pos=(-1.3, 0, 0.9),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=0
        )

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


    def createGameInfo(self):
        # the current phase is displayed at the top of the screen
        self.phase_text = OnscreenText(
            text="memorize",
            pos=(0, 0.85),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=0
        )

        # the countdown is displayed directly below the phase
        self.timer_text = OnscreenText(
            text="20 s",
            pos=(0, 0.75),
            scale=0.06,
            fg=(1, 1, 1, 1),
            align=0
        )

        # the score is only shown after the round has finished
        self.score_text = OnscreenText(
            text="",
            pos=(0, 0.65),
            scale=0.06,
            fg=(1, 1, 1, 1),
            align=0
        )

    def updatePhase(self, phase):
        # update the phase label without recreating the text element
        self.phase_text.setText(phase)

    def updateTimer(self, seconds):
        # display the remaining time as whole seconds
        self.timer_text.setText(f"{seconds} s")

    def showScore(self, score):
        # display the final score after the evaluation
        self.score_text.setText(f"score: {score:g}")

    def updateHighscore(self, score):
        # update the displayed highscore
        self.highscore_text.setText(f"highscore: {score:g}")
