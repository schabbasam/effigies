# contains all models

# thanks to https://opengameart.org/users/theness

from panda3d.core import NodePath
from panda3d.core import CollisionNode, CollisionBox, BitMask32

# this class is the parent of all models
class Model:
    def __init__(self, app, model_path, size, color, scale_factor, interactable=False):

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
        collider_path = self.model.attachNewNode(collision_node)

        self.interactable = interactable
        self.original_color = color
        self.loaded_model = model

        collider_path.setPythonTag("model", self)

    def setPos(self, x, y, z):
        # simplifying positioning
        self.model.setPos(x, y, z)

    def setHighlight(self, enabled):
        if enabled:
            self.loaded_model.setColor(1, 1, 0.3, 1)
        else:
            self.loaded_model.setcolor(*self.original_color)

class Box(Model):
    def __init__(self, app, size, color, interactable=False):
        super().__init__(app, "assets/box.obj", size, color, 2, interactable)

class TexturedBox(Model):
    def __init__(self, app, size, color, interactable=False):
        super().__init__(app, "models/box", size, color, 1, interactable)

