from pathlib import Path
import block_model
import math
from itertools import product
from functools import reduce


def import_block_model_from_file(filename, data_columns, mineral_names):
    new_blocks = block_model.BlockModel()
    if Path(filename).is_file():
        source_file = open(filename, "r")
        file_lines = source_file.readlines()

        for line in file_lines:
            
            block_values = line.split(' ')

            try:
                position_x = int(block_values[data_columns[0]])
                position_y = int(block_values[data_columns[1]])
                position_z = int(block_values[data_columns[2]])
                weight = float(block_values[data_columns[3]])
                new_block = block_model.Block(weight)
                for i in range(4, len(data_columns)):
                    new_block.add_mineral(mineral_names[i-4], float(block_values[data_columns[i]]))
                new_blocks.add_block((position_x, position_y, position_z), new_block)
            except IndexError:
                new_blocks = None

    return new_blocks


def import_block_model_from_json_object(json_object):
    new_block_model = block_model.BlockModel()
    try:
        for i in range(len(json_object['x_positions'])):
            if json_object['x_positions'][i] == '':
                continue
            position_tuple = (int(json_object['x_positions'][i]), int(json_object['y_positions'][i]),
                              int(json_object['z_positions'][i]))
            weight = float(json_object['weights'][i])
            new_block = block_model.Block(weight)
            mineral_grades = json_object['grades']
            for mineral in mineral_grades:
                new_block.add_mineral(mineral, float(mineral_grades[mineral]))
            new_block_model.add_block(position_tuple, new_block)
        return new_block_model
    except TypeError:
        return None


def get_reblock_dimensions(current_block_model, blocks_to_group_tuple):
    width, depth, height = current_block_model.get_model_dimensions()
    reblock_width = int(math.ceil(width / float(blocks_to_group_tuple[0])))
    reblock_depth = int(math.ceil(depth / float(blocks_to_group_tuple[1])))
    reblock_height = int(math.ceil(height / float(blocks_to_group_tuple[2])))
    return reblock_width, reblock_depth, reblock_height


def group_block_with_surrounding_blocks(current_block_model, starting_position_tuple, blocks_to_group_tuple):
    block_indexes_upper_range = (starting_position_tuple[0] + blocks_to_group_tuple[0],
                                 starting_position_tuple[1] + blocks_to_group_tuple[1],
                                 starting_position_tuple[2] + blocks_to_group_tuple[2])
    blocks_to_group_indexes = list(product(range(starting_position_tuple[0], block_indexes_upper_range[0]),
                                           range(starting_position_tuple[1], block_indexes_upper_range[1]),
                                           range(starting_position_tuple[2], block_indexes_upper_range[2])))
    blocks_to_group = list(map(lambda x: current_block_model.get_block_at_position(x), blocks_to_group_indexes))
    block_group = block_model.BlockGroup()
    list(map(lambda x: block_group.add_block(x), blocks_to_group))
    return block_group


def group_model_block_into_new_model(current_block_model, new_model, blocks_to_group_tuple,
                                     new_model_block_index_tuple):
    starting_block_position = (new_model_block_index_tuple[0] * blocks_to_group_tuple[0],
                               new_model_block_index_tuple[1] * blocks_to_group_tuple[1],
                               new_model_block_index_tuple[2] * blocks_to_group_tuple[2])
    virtual_block = group_block_with_surrounding_blocks(current_block_model, starting_block_position,
                                                        blocks_to_group_tuple)
    new_model.add_block(new_model_block_index_tuple, virtual_block)


def virtual_reblock_model(current_block_model, blocks_to_group_tuple):
    reblock_width, reblock_depth, reblock_height = get_reblock_dimensions(current_block_model, blocks_to_group_tuple)
    virtual_reblocked_model = block_model.BlockModel()
    virtual_blocks_model_indexes = list(product(range(reblock_width), range(reblock_depth), range(reblock_height)))
    list(map(lambda x: group_model_block_into_new_model(current_block_model, virtual_reblocked_model,
                                                        blocks_to_group_tuple, x), virtual_blocks_model_indexes))
    return virtual_reblocked_model
