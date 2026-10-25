
import random
import colors

class Generator:
    def __init__(self, block_manger):
        self.block_manager = block_manger

    def generate(self, count=16):
        structure = {}
        positions = [
            (x, y, 0)
            for x in range(self.block_manager.island.grid_size)
            for y in range(self.block_manager.island.grid_size)
        ]

        random.shuffle(positions)

        count = min(count, len(positions))

        for pos in positions[:count]:
            color = random.choice(colors.LIST)
            structure[pos] = color

        return structure

    def build(self, structure):
        for pos, color in structure.items():
            self.block_manager.placeBlock(pos, variant=color)
