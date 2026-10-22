# this file contains everything about the camera

from direct.task import Task
from panda3d.core import WindowProperties

class CameraController:
    def __init__(self, app):
        # we need to do this because this class does not inherit from ShowBase
        self.app = app

        # disabling the default camera controls (function name is a lil misleading)
        self.app.disableMouse()
        
        # heading is left/right, pitch is up/down
        self.heading    = 0.0
        self.pitch      = 0.0
        self.sensitivity = 80.0

        p = WindowProperties()
        # M_confined is responsible for keeping the mouse inside the window
        p.setMouseMode(WindowProperties.M_confined)
        p.setCursorHidden(True)
        # this function requests the change
        self.app.win.requestProperties(p)
        
        # this calls resolveMouse after the window settings have been set properly
        # basically it waits until the requestProperties is finished I guess
        # otherwise i wouldn't work and you'd get a nasty error
        # the 0 means 0s delay, but the actual purpose is to execute the function in the next task
        self.app.taskMgr.doMethodLater(0, self.resolveMouse, "resolve-mouse")

    def resolveMouse(self, task):
        # initalize the mouse
        self.lastX = None
        self.lastY = None
        self.app.taskMgr.add(self.updateCamera, "camera")

        # although resolveMouse is a task, it's meant to be executed only once
        return task.done

    def updateLook(self):
        watcher = self.app.mouseWatcherNode
        
        # the mouseWatcherNode gives normalized positions
        # the values are between -1.0 (far right/bottom) and 1.0 (far left/top)
        x = watcher.getMouseX()
        y = watcher.getMouseY()

        if self.lastX is not None:
            deltaX = x - self.lastX
            deltaY = y - self.lastY
        else:
            deltaX, deltaY = 0.0, 0.0

        self.lastX = x
        self.lastY = y
        
        self.heading    -= deltaX * self.sensitivity
        self.pitch      += deltaY * self.sensitivity

        self.pitch = max(-90.0, min(90.0, self.pitch))

        self.app.camera.setHpr(self.heading, self.pitch, 0)

    def updateCamera(self, task):
        self.updateLook()
        return task.cont
