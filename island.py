# this class contains the island and game grid

from models import Box, TexturedBox

class Island:
    def __init__(self, app, grid_size=5):
        self.app = app
        self.grid_size = grid_size

        self.nodes = []

        self.createIsland()
        self.createGrid()

    def createIsland(self):
        
        green = (0.25, 0.65, 0.25, 1)
        brown = (0.35, 0.22, 0.12, 1)

        dirt = Box(self.app, (10, 10, 1), brown)
        dirt.setPos(0, 0, -0.8)

        grass = TexturedBox(self.app, (10, 10, 0.3), green)
        grass.setPos(0, 0, -0.15)

        a = Box(self.app, (0.2, 0.2, 1), brown)
        a.setPos(0, 0, 0.5)

        self.nodes.append(dirt)
        self.nodes.append(grass)

    def createGrid(self):
        grid_size = 5
        tile_size = 0.5
        tile_height = 0.1
        grid_z = tile_height / 2

        tile_color = (0.3, 0.7, 0.3, 1)

        for row in range(grid_size):
            for column in range(grid_size):
                tile = Box(
                        self.app,
                        (tile_size, tile_size, tile_height),
                        tile_color
                )
                x = (column - (grid_size - 1) / 2) * tile_size
                y = (row - (grid_size - 1) / 2) * tile_size

                tile.setPos(x, y, grid_z)

    def destroy(self):

        for node in self.nodes:
            node.removeNode()

        self.nodes.clear()


