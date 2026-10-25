# this class contains the island and game grid

from block_manager import BlockManager
from models import Box, TexturedBox
import colors

class Island:
    def __init__(self, app):
        self.app = app
        self.grid_size = 5

        self.nodes = []
        self.grid = {}

        self.createIsland()
        self.createGrid()

        self.block_manager = BlockManager(self)

    def createIsland(self):
        
        dirt = Box(self.app, (10, 10, 1), colors.DIRT)
        dirt.setPos(0, 0, -0.8)

        grass = TexturedBox(self.app, (10, 10, 0.3), colors.GRASS)
        grass.setPos(0, 0, -0.15)

        self.nodes.append(dirt)
        self.nodes.append(grass)

    def createGrid(self):
        tile_size = 0.5
        tile_height = 0.1
        grid_z = tile_height / 2

        tile_color = colors.TILE

        for row in range(self.grid_size):
            for column in range(self.grid_size):
                tile = Box(
                        self.app,
                        (tile_size, tile_size, tile_height),
                        tile_color,
                        interactable=True
                )
                x = (column - (self.grid_size - 1) / 2) * tile_size
                y = (row - (self.grid_size - 1) / 2) * tile_size

                tile.setPos(x, y, grid_z)

                # map each tile to its logical grid coordinates
                self.grid[tile] = (column, row)
                self.nodes.append(tile)

    def destroy(self):

        for node in self.nodes:
            node.removeNode()

        self.nodes.clear()
        self.grid.clear()
        self.block_manager.blocks.clear()

