# this class contains the island and game grid

from models import Box, TexturedBox
import colors

class Island:
    def __init__(self, app, grid_size=5):
        self.app = app
        self.grid_size = grid_size

        self.nodes = []

        self.createIsland()
        self.createGrid()

    def createIsland(self):
        
        dirt = Box(self.app, (10, 10, 1), colors.DIRT)
        dirt.setPos(0, 0, -0.8)

        grass = TexturedBox(self.app, (10, 10, 0.3), colors.GRASS)
        grass.setPos(0, 0, -0.15)

        self.nodes.append(dirt)
        self.nodes.append(grass)

    def createGrid(self):
        grid_size = 5
        tile_size = 0.5
        tile_height = 0.1
        grid_z = tile_height / 2

        tile_color = colors.LIST[0]

        for row in range(grid_size):
            for column in range(grid_size):
                tile = Box(
                        self.app,
                        (tile_size, tile_size, tile_height),
                        tile_color,
                        interactable=True
                )
                x = (column - (grid_size - 1) / 2) * tile_size
                y = (row - (grid_size - 1) / 2) * tile_size

                tile.setPos(x, y, grid_z)

    def destroy(self):

        for node in self.nodes:
            node.removeNode()

        self.nodes.clear()


