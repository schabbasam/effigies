# handles all interactions with game elements

from panda3d.core import (
        CollisionNode,
        CollisionRay,
        CollisionHandlerQueue,
        CollisionTraverser,
        BitMask32
)

class Interactor:
    def __init__(self, app, island):
        self.app = app
        self.island = island

        self.hovered_model = None
        self.block_manager = island.block_manager
        self.hovered_normal = None

        # relevant for placing blocks
        self.selected_block = 0
        self.selected_variant = 0

        # create ray from the center of the camera
        self.ray = CollisionRay()
        ray_node = CollisionNode("interaction_ray")

        # addSolid adds the ray as a form of collision
        ray_node.addSolid(self.ray)

        # collides with every bit(1) entity, but never gets targeted by others
        ray_node.setFromCollideMask(BitMask32.bit(1))
        ray_node.setIntoCollideMask(BitMask32.allOff())

        # makes the ray move with the camera and point through the center of the screen
        self.ray_path = self.app.camera.attachNewNode(ray_node)
        self.ray.setFromLens(self.app.camNode, 0, 0)

        # the traverser checks for collisions
        self.traverser = CollisionTraverser()
        # the queue saves all hits in a list
        self.queue = CollisionHandlerQueue()
        # they both get connected
        self.traverser.addCollider(self.ray_path, self.queue)

        self.app.accept("mouse1", self.placeBlock)
        self.app.accept("mouse3", self.removeBlock)

        self.app.taskMgr.add(self.update, "interaction_update")

    def update(self, task):
        # traverser checks the ray for any collisions with objects under render (basically whole game)
        self.traverser.traverse(self.app.render)

        # sorts the entries by distance, the closest collision is the first
        self.queue.sortEntries()

        valid_model = None
        valid_normal = None
        
        # getNumEntries returns the number of entries
        if self.queue.getNumEntries() > 0:
            # we only need the first entry because it covers the others
            entry = self.queue.getEntry(0)
            collider = entry.getIntoNodePath()
            
            # remember: the python tag with the key "model" references itself
            # you can identify a model with this tag basically
            if collider.hasPythonTag("model"):
                model = collider.getPythonTag("model")

                if model.interactable:
                    valid_model = model
                    valid_normal = entry.getSurfaceNormal(self.app.render)

        # if the target (hovered_model) from last time changed
        if valid_model != self.hovered_model:
            # note: None means you are aiming at a non interactable thing

            # if the previous target exists...
            if self.hovered_model is not None:
                # ...remove the highlight from it
                self.hovered_model.setHighlight(False)
            
            # if the new target exists...
            if valid_model is not None:
                # ...turn the highlight on
                valid_model.setHighlight(True)
            
            # remembers the target change
            self.hovered_model = valid_model
        
        self.hovered_normal = valid_normal

        # clear entries for the next task loop
        self.queue.clearEntries()

        return task.cont

    def placeBlock(self):
        # it reuses the hovered_model determined by the update loop
        # instead of casting a second ray
        if self.hovered_model is None or self.hovered_normal is None:
            return

        normal = self.hovered_normal

        direction = (
                round(normal.x),
                round(normal.y),
                round(normal.z)
        )

        if self.hovered_model in self.island.grid:
            x, y = self.app.island.grid[self.hovered_model]

            if direction[2] > 0:
                pos = (x, y, 0)
            else:
                pos = (
                        x + direction[0],
                        y + direction[1],
                        0
                )
            
        elif hasattr(self.hovered_model, "block_pos"):
            x, y, z = self.hovered_model.block_pos

            pos = (
                    x + direction[0],
                    y + direction[1],
                    z + direction[2]
            )

        else:
            return

        self.block_manager.placeBlock(
                pos,
                self.selected_block,
                self.selected_variant
        )

    def removeBlock(self):
        if self.hovered_model is None:
            return

        if not hasattr(self.hovered_model, "block_pos"):
            return

        pos = self.hovered_model.block_pos

        if self.block_manager.removeBlock(pos):
            self.hovered_model = None
            self.hovered_normal = None
