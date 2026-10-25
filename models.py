# Contains all models.

from pathlib import Path
import sys

from panda3d.core import NodePath
from panda3d.core import CollisionNode, CollisionBox, BitMask32


class Model:
    def __init__(self, app, model_path, size, color, scale_factor, interactable=False):
        self.color = color

        # Resolve our own assets independently of the directory the game is
        # launched from. Panda3D's built-in models (e.g. "models/box") are
        # still resolved through Panda3D's normal model search path.
        if model_path.startswith("assets/"):
            if getattr(sys, "frozen", False):
                base_path = Path(sys._MEIPASS)
            else:
                base_path = Path(__file__).resolve().parent
            model_path = str(base_path / model_path)

        self.model = app.render.attachNewNode("model")
        model = app.loader.loadModel(model_path)
        model.reparentTo(self.model)

        model.setScale(
            size[0] / scale_factor,
            size[1] / scale_factor,
            size[2] / scale_factor
        )
        model.setColor(self.color[0])

        min_bound, max_bound = model.getTightBounds(self.model)
        center = (min_bound + max_bound) / 2
        model.setPos(model.getPos() - center)

        min_bound, max_bound = model.getTightBounds(self.model)
        collision_node = CollisionNode("block_collider")
        collision_node.addSolid(CollisionBox(min_bound, max_bound))
        collision_node.setIntoCollideMask(BitMask32.bit(1))

        collider_path = self.model.attachNewNode(collision_node)
        self.interactable = interactable
        self.loaded_model = model
        collider_path.setPythonTag("model", self)

    def setPos(self, x, y, z):
        self.model.setPos(x, y, z)

    def setHighlight(self, enabled):
        if enabled:
            self.loaded_model.setColor(self.color[1])
        else:
            self.loaded_model.setColor(self.color[0])

    def removeNode(self):
        self.model.removeNode()


class Box(Model):
    def __init__(self, app, size, color, interactable=False):
        super().__init__(app, "assets/box.obj", size, color, 2, interactable)


class TexturedBox(Model):
    def __init__(self, app, size, color, interactable=False):
        super().__init__(app, "models/box", size, color, 1, interactable)
