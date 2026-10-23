# this file contains everything about the camera

from math import sin, cos, radians

from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import WindowProperties, Vec3

class CameraController:
    def __init__(self, app, settings):
        # we need to do this because this class does not inherit from ShowBase
        self.app = app

        self.settings = settings

        # this variable is necessary to reset the coordinates properly after recentering
        # because mouseWatchNode does not get the input immediatly
        self.ignore_next_mouse_delta = False

        # disabling the default camera controls (function name is a lil misleading)
        self.app.disableMouse()
        
        # heading is left/right, pitch is up/down
        self.heading    = 0.0
        self.pitch      = 0.0
        
        self.key_states = {}
        self.sensitivity = self.settings.sensitivity
        
        self.setupLook()
        self.setupMovement()
    
    def setupLook(self):
        
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

    def setupMovement(self):
        # dict with every keybind and boolean value for pressed/not pressed
        self.key_states = {key: False for key in self.settings.keybinds.values()}

        for key in self.key_states.keys():
            # set the key to adjust the key_states if pressed/released
            self.app.accept(key, self.setKeys, [key, True])
            self.app.accept(key + "-up", self.setKeys, [key, False])

    def setKeys(self, key, value):
        self.key_states[key] = value
        

    def resolveMouse(self, task):
        # initalize the mouse
        self.lastX = None
        self.lastY = None
        self.app.taskMgr.add(self.updateCamera, "camera")

        # although resolveMouse is a task, it's meant to be executed only once
        return task.done

    def recenterMouse(self):
        # recentering the cursor is crucial because the mouse hits the edge of the window

        p = self.app.win.getProperties()

        centerX = p.getXSize() // 2
        centerY = p.getYSize() // 2
        
        self.app.win.movePointer(0, centerX, centerY)
        self.ignore_next_mouse_delta = True

    def updateLook(self):
        watcher = self.app.mouseWatcherNode
        
        # the mouseWatcherNode gives normalized positions
        # the values are between -1.0 (far right/bottom) and 1.0 (far left/top)
        x = watcher.getMouseX()
        y = watcher.getMouseY()
        
        if self.ignore_next_mouse_delta:
            self.lastX = x
            self.lastY = y
            self.ignore_next_mouse_delta = False
            return

        if self.lastX is not None:
            deltaX = x - self.lastX
            deltaY = y - self.lastY
        else:
            deltaX, deltaY = 0.0, 0.0

        self.lastX = x
        self.lastY = y
        
        self.heading    -= deltaX * self.sensitivity
        self.pitch      += deltaY * self.sensitivity
        
        # prevents the camera from turning upside down
        self.pitch = max(-90.0, min(90.0, self.pitch))

        self.app.camera.setHpr(self.heading, self.pitch, 0)

        self.recenterMouse()

    def updateMovement(self):
        # the time delta
        delta = globalClock.getDt()
        
        heading = radians(self.app.camera.getH())
        
        forward = Vec3(-sin(heading), cos(heading), 0)
        right = Vec3(cos(heading), sin(heading), 0)

        movement = Vec3(0, 0, 0)

        kb = self.settings.keybinds

        if self.key_states[kb["forward"]]:
            movement += forward
        if self.key_states[kb["backward"]]:
            movement -= forward
        if self.key_states[kb["right"]]:
            movement += right
        if self.key_states[kb["left"]]:
            movement -= right
        if self.key_states[kb["up"]]:
            movement.z += 1
        if self.key_states[kb["down"]]:
            movement.z -= 1

        # if movement is not empty
        if movement.lengthSquared() > 0:
            # prevents the movement from being 1.41 * faster diagonally
            movement.normalize()

            self.app.camera.setPos(
                    self.app.camera.getPos()
                    + movement * delta * self.settings.speed)
            # multiplying with delta makes the speed independant from the frame rate

    def updateCamera(self, task):
        self.updateLook()
        self.updateMovement()
        return task.cont
