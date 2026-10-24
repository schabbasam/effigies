# contains all models

# thanks to https://opengameart.org/users/theness

from panda3d.core import NodePath
from panda3d.core import CollisionNode, CollisionBox, BitMask32

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
                size[2] / scale_factor
        )

        # setting the color
        model.setColor(*color)
        
        # centering the origin (place where coordinates are measured)
        min_bound, max_bound = model.getTightBounds(self.model)
        center = (min_bound + max_bound) / 2
        model.setPos(model.getPos() -center)

        # calculating bounds after recentering in the parent's coordinates
        min_bound, max_bound = model.getTightBounds(self.model)

        # set up collision
        collision_node = CollisionNode("block_collider")

        # this creates an invisible collision box
        collision_node.addSolid(CollisionBox(min_bound, max_bound))

        # marks the block as something collidable
        # bit(1) is just a preset category
        collision_node.setIntoCollideMask(BitMask32.bit(1))
        
        # sets the model as a parent of collision_node
        # that means it will move with it
        self.model.attachNewNode(collision_node)

    def setPos(self, x, y, z):
        # simplifying positioning
        self.model.setPos(x, y, z)

class Box(Model):
    def __init__(self, app, size, color):
        super().__init__(app, "assets/box.obj", size, color, 2)

class TexturedBox(Model):
    def __init__(self, app, size, color):
        super().__init__(app, "models/box", size, color, 1)

