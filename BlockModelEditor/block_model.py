class MineralDeposit:

    def __init__(self, name):
        self.name = name
        self.block_models = []

    def add_block_model(self, block_model):
        self.block_models.append(block_model)


class VirtualBlock:

    @property
    def weight(self):
        raise NotImplementedError

    def mineral_grade(self, mineral_name):
        raise NotImplementedError

    @property
    def mineral_names(self):
        raise NotImplementedError


class Block(VirtualBlock):

    def __init__(self, weight):
        self._weight = weight
        self._minerals = {}

    @property
    def weight(self):
        return self._weight

    @property
    def mineral_names(self):
        names = []
        for mineral_name in self._minerals:
            names.append(mineral_name)
        return names

    def mineral_grade(self, mineral_name):
        if mineral_name in self._minerals:
            return self._minerals[mineral_name]
        return 0

    def add_mineral(self, mineral_name, grade):
        self._minerals[mineral_name] = grade


class BlockGroup(VirtualBlock):

    def __init__(self):
        self.blocks = []

    @property
    def weight(self):
        weights = map(lambda x: x.weight, self.blocks)
        return sum(weights)

    @property
    def mineral_names(self):
        all_names = map(lambda x: x.mineral_names, self.blocks)
        names_without_repeats = []
        map(lambda x: map(lambda y: names_without_repeats.append(y) if y not in names_without_repeats else None, x),
            all_names)
        return names_without_repeats

    def mineral_grade(self, mineral_name):
        weighted_grades = map(lambda x: x.weight * x.mineral_grade(mineral_name), self.blocks)
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
            value = Block(0)
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
            dimensions = self.get_model_dimensions()
            for i in range(dimensions[0]):
                for j in range(dimensions[1]):
                    for k in range(dimensions[2]):
                        if self.get_block_at_position((i, j, k)).weight == 0:
                            air_block_count += 1
            total_spaces = dimensions[0] * dimensions[1] * dimensions[2]
            air_proportion = air_block_count / total_spaces
        return 100 * air_proportion

    def get_all_minerals(self):
        names = []
        for position in self.blocks:
            for mineral_name in self.blocks[position].mineral_names:
                if mineral_name not in names:
                    names.append(mineral_name)
        return names

    def get_total_mineral_grade(self, mineral_name):
        total_grade = 0
        for position in self.blocks:
            total_grade += self.blocks[position].mineral_grade(mineral_name)
        return total_grade

    def get_total_grades(self):
        grades = {}
        mineral_names = self.get_all_minerals()
        for mineral_name in mineral_names:
            grades[mineral_name] = self.get_total_mineral_grade(mineral_name)
        return grades
