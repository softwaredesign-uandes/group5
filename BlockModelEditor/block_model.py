class VirtualBlock:

    @property
    def weight(self):
        raise NotImplementedError

    @property
    def grade(self):
        raise NotImplementedError


class Block(VirtualBlock):

    def __init__(self, weight, grade):
        self._weight = weight
        self._grade = grade

    @property
    def weight(self):
        return self._weight

    @property
    def grade(self):
        return self._grade


class BlockGroup(VirtualBlock):

    def __init__(self):
        self.blocks = []

    @property
    def weight(self):
        weights = map(lambda x: x.weight, self.blocks)
        return sum(weights)

    @property
    def grade(self):
        weighted_grades = map(lambda x: x.weight * x.grade, self.blocks)
        weight = self.weight
        return sum(weighted_grades) / weight if weight > 0 else 0

    def add_block(self, block):
        self.blocks.append(block)

    def remove_block(self, block):
        self.blocks.remove(block)

    def block_count(self):
        return len(self.blocks)


class BlockModel:

    def __init__(self):
        self.blocks = {}

    def add_block(self, position_tuple, block):
        self.blocks[position_tuple] = block

    def get_block_at_position(self, position_tuple):
        try:
            value = self.blocks[position_tuple]
        except KeyError:
            value = None
        return value

    def get_total_block_number(self):
        return len(self.blocks)

    def get_model_dimensions(self):
        max_position_x = 0
        max_position_y = 0
        max_position_z = 0
        if self.get_total_block_number() == 0:
            return max_position_x, max_position_y, max_position_z
        for position in self.blocks:
            if position[0] > max_position_x:
                max_position_x = position[0]
            if position[1] > max_position_y:
                max_position_y = position[1]
            if position[2] > max_position_z:
                max_position_z = position[2]
        return max_position_x + 1, max_position_y + 1, max_position_z + 1

    def get_total_weight(self):
        total_weight = 0
        for position in self.blocks:
            total_weight += self.blocks[position].weight
        return total_weight

    def get_air_percentage(self):
        air_block_count = 0
        total_blocks = self.get_total_block_number()
        air_proportion = 1
        if total_blocks > 0:
            for position in self.blocks:
                if self.blocks[position].weight == 0:
                    air_block_count += 1
            air_proportion = air_block_count / total_blocks
        return 100 * air_proportion

    def get_total_grade(self):
        total_grade = 0
        for position in self.blocks:
            total_grade += self.blocks[position].grade
        return total_grade
