# contains all models

# thanks to https://opengameart.org/users/theness

from panda3d.core import NodePath

class Box:
    def __init__(self, app, size, color):
        
        self.model = app.render.attachNewNode("box")

        model = app.loader.loadModel("assets/box.obj")
        model.reparentTo(self.model)
        
        model.setScale(size[0] / 4,
                       size[1] / 4,
                       size[2] / 4)
        
        min_bound, max_bound = model.getTightBounds()
        center = (min_bound + max_bound) / 2
        model.setPos(-center)

        model.setColor(*color)

    def setPos(self, x, y, z):
        self.model.setPos(x, y, z)

class TexturedBox:
    def __init__(self, app, size, color):
        self.model = app.render.attachNewNode("box2")

        model = app.loader.loadModel("models/box")
        model.reparentTo(self.model)
        
        model.setScale(size[0] / 2,
                       size[1] / 2,
                       size[2] / 2)

        min_bound, max_bound = model.getTightBounds()
        center = (min_bound + max_bound) / 2
        model.setPos(-center)

        model.setColor(*color)

    def setPos(self, x, y, z):
        self.model.setPos(x, y, z)


