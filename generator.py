
import random
import colors

class Generator:
    def __init__(self, block_manger):
        self.block_manager = block_manger

        self.directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]

    def generate(self):
        count = self.block_manager.island.app.save_manager.data()["settings"]["difficulty"]
        structure = {}
        positions = [
            (x, y, z)
            for x in range(self.block_manager.island.grid_size)
            for y in range(self.block_manager.island.grid_size)
            for z in range(self.block_manager.max_height)
        ]

        random.shuffle(positions)

        count = min(count, len(positions))

        for pos in positions[:count]:
            color = random.choice(colors.LIST)
            structure[pos] = color

        return self.removeHiddenBlocks(structure)

    def build(self, structure):
        for pos, color in structure.items():
            self.block_manager.placeBlock(pos, variant=color)

    def removeHiddenBlocks(self, structure):
        remove = []

        for x, y, z in structure:
            has_free_side = False

            for dx, dy, dz in self.directions:
                neighbor = (x + dx, y + dy, z + dz)

                if neighbor not in structure:
                    has_free_side = True
                    break

            if not has_free_side:
                remove.append((x, y, z))

        for pos in remove:
            del structure[pos]

        return structure    
