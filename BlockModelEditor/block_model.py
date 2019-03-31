class Block:

    def __init__(self, position_x, position_y, position_z, weight, grade):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.weight = weight
        self.grade = grade

    def get_position(self):
        return self.position_x, self.position_y, self.position_z
