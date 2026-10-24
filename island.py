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

        earth = Box(self.app, (20, 20, 1), brown)
        earth.setPos(0, 0, -0.8)

        grass = TexturedBox(self.app, (19, 19, 0.3), green)
        grass.setPos(0, 0, -0.15)

        a = Box(self.app, (0.001, 0.001, 0.01), (1, 1, 1, 1))
        a.setPos(1, 1, 0)

        self.nodes.append(earth)
        self.nodes.append(grass)

    def createGrid(self):
        pass

    def destroy(self):

        for node in self.nodes:
            node.removeNode()

        self.nodes.clear()


