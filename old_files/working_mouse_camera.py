
import sys

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties


class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.lastMouseX = None
        self.lastMouseY = None

        self.yaw = 0.0
        self.pitch = 0.0
        self.sensitivity = 80.0

        props = WindowProperties()
        props.setMouseMode(WindowProperties.M_confined)
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        self.accept("escape", sys.exit)
        
        block = self.loader.loadModel("models/box")
        block.reparentTo(self.render)
        block.setScale(60, 60, 1)
        block.setPos(-29, -32, 0)

        self.camera.setPos(3, -3, 4)
        self.camera.lookAt(0, 0, 0.5)

        self.yaw = self.camera.getH()
        self.pitch = self.camera.getP()

        self.taskMgr.doMethodLater(
            0, self.resolveMouse, "resolve-mouse"
        )

    def resolveMouse(self, task):
        self.recenterMouse()
        self.lastMouseX = None
        self.lastMouseY = None
        self.taskMgr.add(self.updateCamera, "camera")
        return Task.done

    def recenterMouse(self):
        props = self.win.getProperties()
        self.win.movePointer(
            0, props.getXSize() // 2, props.getYSize() // 2
        )

    def updateCamera(self, task):
        watcher = self.mouseWatcherNode

        x = watcher.getMouseX()
        y = watcher.getMouseY()

        if self.lastMouseX is not None:
            dx = x - self.lastMouseX
            dy = y - self.lastMouseY
        else:
            dx, dy = 0.0, 0.0

        self.lastMouseX, self.lastMouseY = x, y


        self.yaw -= dx * self.sensitivity
        self.pitch += dy * self.sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))

        self.camera.setHpr(self.yaw, self.pitch, 0)
        return Task.cont


Game().run()

