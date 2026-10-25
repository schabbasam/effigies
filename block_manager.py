
import colors
from models import Box

from panda3d.core import (
        CollisionBox,
        CollisionNode,
        BitMask32,
        Point3
)

class BlockManager:
    def __init__(self, island):
        self.island = island
        self.app = island.app
        self.max_height = 3

        # (x, y, z): Box
        self.blocks = {}

    def isValidPos(self, pos):
        x, y, z = pos
        
        # if all 3 coordinates are in the valid range, it returns True
        return (
            0 <= x < self.island.grid_size
            and 0 <= y < self.island.grid_size
            and 0 <= z < self.max_height
        )

    def getBlock(self, pos):
        # simply returns which block is at pos
        # we use .get() because it doesn't throw a tantrum if the key doesn't exist
        return self.blocks.get(tuple(pos))

    def placeBlock(self, pos, block_type=0, variant=0):

        # this just turns a list into a tuple
        # doesn't really matter tho because we just insert a tuple
        pos = tuple(pos)
        
        # if it isn't a valid position or if there already is a block,
        # the function is over and returns None, meaning nothing got placed
        if not self.isValidPos(pos):
            return None

        if pos in self.blocks:
            return None

        # basic block for the MVP
        # different block types can be added later 
        block = Box(
            self.app,
            (0.5, 0.5, 0.5),
            colors.LIST[4],
            interactable=True
        )

        x, y, z = pos

        # grid is centered at the origin
        # each grid cell is 0.5 units wide
        world_x = (x - (self.island.grid_size - 1) / 2) * 0.5
        world_y = (y - (self.island.grid_size - 1) / 2) * 0.5

        # top of the grass is at z = 0
        # each block occupies 0.5 units in height
        world_z = 0.35 + z * 0.5

        block.setPos(world_x, world_y, world_z)

        # store logical coordinates on the model itself
        block.block_pos = pos
        
        # adding the block to the dictionary and island node
        self.blocks[pos] = block
        self.island.nodes.append(block)

        # we can use this return value later to check if a block got placed or not
        return block

    def removeBlock(self, pos):
        pos = tuple(pos)

        # removes and returns the key and value
        # if there isn't a key, it returns None to prevent a KeyError
        block = self.blocks.pop(pos, None)

        # returns False if no block got removed (because there was no block there)
        # the caller knows nothing changed
        if block is None:
            return False
        
        # remove it from the SceneGraph with the function we wrote in models.py
        block.removeNode()
        
        # removes block from the dictionary
        # this case distinction just double checks if the block is actually in the dictionary
        if block in self.island.nodes:
            self.island.nodes.remove(block)

        # returns that it was a succes (that a block got deleted)
        return True
