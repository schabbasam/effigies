# handles all interactions with game elements

from panda3d.core import (
        CollisionNode,
        CollisionRay,
        CollisionHandlerQueue,
        CollisionTraverser,
        BitMask32
)

class Interactor:
    def __init__(self, app):
        self.app = app
        self.hovered_model = None

        # create ray from the center of the camera
        self.ray = CollisionRay()
        ray_node = CollisionNode("interaction_ray")
        ray_node.addSolid(self.ray)
        ray_node.setFromCollideMask(BitMask32.bit(1))
        ray_node.setIntoCollideMask(BitMask32.allOff())

        self.ray_path = self.app.camera.attachNewNode(ray_node)
        self.ray.setFromLens(self.app.camNode, 0, 0)

        # collision detection
        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        self.traverser.addCollider(self.ray_path, self.queue)

        self.app.accept("mouse1", self.onClick)
        self.app.taskMgr.add(self.update, "interaction_update")

    def update(self, task):
        self.traverser.traverse(self.app.render)
        self.queue.sortEntries()

        new_model = None

        for i in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(i)
            collider = entry.getIntoNodePath()

            if not collider.hasPythonTag("model"):
                continue

            model = collider.getPythonTag("model")

            if model.interactable:
                new_model = model
                break

        if new_model != self.hovered_model:
            if self.hovered_model:
                self.hovered_model.setHighlight(True)
            
            self.hovered_model = new_model

            if self.hovered_model:
                self.hovered_model.setHighlight(True)

        self.queue.clearEntries()

        return task.cont

    def onClick(self):
        if self.hovered_model:
            print("clicked:", self.hovered_model)
