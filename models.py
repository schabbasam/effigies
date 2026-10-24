# contains all models

# thanks to https://opengameart.org/users/theness

from panda3d.core import NodePath

# this class is the parent of all models
class Model:
    def __init__(self, app, model_path, size, color, scale_factor):

        # properly loading the model
        self.model = app.render.attachNewNode("model")
        model = app.loader.loadModel(model_path)
        model.reparentTo(self.model)
        
        # scale everything uniformly
        model.setScale(
                size[0] / scale_factor,
                size[1] / scale_factor,
                size[3] / scale_factor
        )
        
        # centering the origin (place where coordinates are measured)
        min_bound, max_bound = model.getTightBounds()
        center = (min_bound + max_bound) / 2
        model.setPos(-center)

        # setting the color
        model.setColor(*color)

    def setPos(self, x, y, z):
        # simplifying positioning
        self.model.setPos(x, y, z)

class Box(Model):
    def __init__(self, app, size, color):
        super().__init__(app, "assets/box.obj", size, color, 4)

class TexturedBox(Model):
    def __init__(self, app, size, color):
        super().__init__(app, "models/box", size, color, 2)

