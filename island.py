# this class contains the island and game grid

from models import Box, TexturedBox

class Island:
    def __init__(self, app, grid_size=5):
        self.app = app
        self.grid_size = grid_size

        self.nodes = []

        self.createIsland()
#       self.createGrid()

    def createIsland(self):
        
        green = (0.25, 0.65, 0.25, 1)
        brown = (0.35, 0.22, 0.12, 1)

        island = Box(self.app, (1, 1, 1), brown)
        island.setPos(0, 0, 0)

        grass = TexturedBox(self.app, (1, 1, 1), green)
        grass.setPos(0, 0, 0)

        a = Box(self.app, (0.001, 0.001, 0.01), (1, 1, 1, 1))
        a.setPos(1, 1, 0)

        self.nodes.append(island)
        self.nodes.append(grass)

    def createGrid(self):
        grid_width = self.grid_size
        line_thickness = 0.025
        line_height = 0.01

        for i in range(self.grid_size + 1):
            offset = -grid_width / 2 + i

            self.createLine(
                    x=offset,
                    y=0,
                    width=line_thickness,
                    depth=grid_width
            )

            self.createLine(
                    x=0,
                    y=offset,
                    width=grid_width,
                    depth=line_thickness
            )

    def createLine(self, x, y, width, depth):
        line = self.loader.loadModel("models/box")
        line.reparentTo(self.parent)

        line.setScale(
                width / 2,
                depth / 2,
                0.005
        )

        line.setPos(x, y, 0.055)
        line.setColor(0.12, 0.6, 0.12, 1)

        self.nodes.append(line)

    def destroy(self):

        for node in self.nodes:
            node.removeNode()

        self.nodes.clear()


