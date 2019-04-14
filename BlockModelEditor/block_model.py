class Block:

    def __init__(self, weight, grade):
        self.weight = weight
        self.grade = grade


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
        for position in self.blocks:
            if position[0] > max_position_x:
                max_position_x = position[0]
            if position[1] > max_position_y:
                max_position_y = position[1]
            if position[2] > max_position_z:
                max_position_z = position[2]
        return max_position_x, max_position_y, max_position_z

    def get_total_weight(self):
        total_weight = 0
        for position in self.blocks:
            total_weight += self.blocks[position].weight
        return total_weight

    def get_air_percentage(self):
        air_block_count = 0
        for position in self.blocks:
            if self.blocks[position].weight == 0:
                air_block_count += 1
        return 100 * (air_block_count / self.get_total_block_number())

    def get_total_grade(self):
        total_grade = 0
        for position in self.blocks:
            total_grade += self.blocks[position].grade
        return total_grade
