from pathlib import Path
import block_model
import math
from itertools import product
from functools import reduce


def import_block_model_from_file(filename, data_columns):
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
                grade = 0
                for i in range(4, len(data_columns)):
                    grade += float(block_values[data_columns[i]])
                new_blocks.add_block((position_x, position_y, position_z), block_model.Block(weight, grade))
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
            grade = 0
            for mineral_grades in json_object['grades']:
                grade += float(mineral_grades[i])
            block = block_model.Block(weight, grade)
            new_block_model.add_block(position_tuple, block)
        return new_block_model
    except TypeError:
        return None


def get_user_input():
    print("\n[1] Import new Block Model")
    print("[2] Query current Block Model.")
    print("[3] Quit.")

    return input("\nChoose a command: ")


def get_user_query():
    print("\nWhich information do you want from the loaded model?")
    print("")
    print("[1] Number of blocks.")
    print("[2] Total weight of the Mineral Deposit.")
    print("[3] Percentage of Air blocks (blocks with weight of 0).")
    print("[4] Total mineral weight for all minerals in the Mineral Deposit")
    print("[5] Go Back.")

    return input("\nChoose a command: ")


def get_user_data_columns():
    print("Please indicate in which column of the file the following variables are placed "
          "(separated by spaces, 0-indexed)")
    print("X POSITION | Y POSITION | Z POSITION | TOTAL WEIGHT | MINERAL 1 WEIGHT | MINERAL 2 WEIGHT | ...")

    return input("\nInput: ")


def import_block_model():
    data_columns_input = get_user_data_columns()

    if len(data_columns_input) < 5:
        print("Error: Not enough column indexes inserted.")
        return None

    data_columns = [int(x) for x in data_columns_input.split()]

    input_filename = input("Please insert the source file name: ")

    imported_blocks = import_block_model_from_file(input_filename, data_columns)

    if imported_blocks.get_total_block_number() == 0:
        print("Error importing Block Model.")
        return None
    else:
        print("Block Model imported successfully.")
        return imported_blocks


def query_block_model(current_block_model):
    query = get_user_query()
    while query is not '5':
        if query is '1':
            print("Number of blocks: " + str(current_block_model.get_total_block_number()))

        elif query is '2':
            print("Total weight of Block Model: " + str(current_block_model.get_total_weight()))

        elif query is '3':
            print("Percentage of air blocks in model: " + str(current_block_model.get_air_percentage()))

        elif query is '4':
            print("Total mineral weight of Block Model: " + str(current_block_model.get_total_grade()))

        query = get_user_query()


def get_reblock_dimensions(current_block_model, blocks_to_group_tuple):
    width, depth, height = current_block_model.get_model_dimensions()
    reblock_width = int(math.ceil(width / float(blocks_to_group_tuple[0])))
    reblock_depth = int(math.ceil(depth / float(blocks_to_group_tuple[1])))
    reblock_height = int(math.ceil(height / float(blocks_to_group_tuple[2])))
    return reblock_width, reblock_depth, reblock_height


def reblock_two_blocks(first_block, second_block):
    first_block_weight = first_block.weight if first_block is not None else 0
    first_block_grade = first_block.grade if first_block is not None else 0
    second_block_weight = second_block.weight if second_block is not None else 0
    second_block_grade = second_block.grade if second_block is not None else 0
    new_weight = first_block_weight + second_block_weight
    new_grade = 0
    if new_weight != 0:
        new_grade = (first_block_grade * first_block_weight + second_block_grade * second_block_weight) / new_weight
    return block_model.Block(new_weight, new_grade)


def reblock_block_with_surrounding_blocks(current_block_model, starting_position_tuple, blocks_to_group_tuple):
    block_indexes_upper_range = (starting_position_tuple[0] + blocks_to_group_tuple[0],
                                 starting_position_tuple[1] + blocks_to_group_tuple[1],
                                 starting_position_tuple[2] + blocks_to_group_tuple[2])
    blocks_to_reblock_indexes = list(product(range(starting_position_tuple[0], block_indexes_upper_range[0]),
                                             range(starting_position_tuple[1], block_indexes_upper_range[1]),
                                             range(starting_position_tuple[2], block_indexes_upper_range[2])))
    blocks_to_reblock = list(map(lambda x: current_block_model.get_block_at_position(x), blocks_to_reblock_indexes))
    reblocked_block = reduce((lambda x, y: reblock_two_blocks(x, y)), blocks_to_reblock)
    return reblocked_block


def reblock_model_block_into_new_model(current_block_model, new_model, blocks_to_group_tuple,
                                       new_model_block_index_tuple):
    current_model_block_index_x = new_model_block_index_tuple[0] * blocks_to_group_tuple[0]
    current_model_block_index_y = new_model_block_index_tuple[1] * blocks_to_group_tuple[1]
    current_model_block_index_z = new_model_block_index_tuple[2] * blocks_to_group_tuple[2]
    starting_block_position = (current_model_block_index_x, current_model_block_index_y, current_model_block_index_z)
    reblocked_block = reblock_block_with_surrounding_blocks(current_block_model, starting_block_position,
                                                            blocks_to_group_tuple)
    new_model.add_block(new_model_block_index_tuple, reblocked_block)


def reblock_model(current_block_model, blocks_to_group_tuple):
    reblock_width, reblock_depth, reblock_height = get_reblock_dimensions(current_block_model, blocks_to_group_tuple)
    reblocked_model = block_model.BlockModel()
    reblocked_model_indexes = list(product(range(reblock_width), range(reblock_depth), range(reblock_height)))

    list(map(lambda x: reblock_model_block_into_new_model(current_block_model, reblocked_model, blocks_to_group_tuple,
                                                          x), reblocked_model_indexes))

    return reblocked_model


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
    virtual_block = reblock_block_with_surrounding_blocks(current_block_model, starting_block_position,
                                                          blocks_to_group_tuple)
    new_model.add_block(new_model_block_index_tuple, virtual_block)


def virtual_reblock_model(current_block_model, blocks_to_group_tuple):
    reblock_width, reblock_depth, reblock_height = get_reblock_dimensions(current_block_model, blocks_to_group_tuple)
    virtual_reblocked_model = block_model.BlockModel()
    virtual_blocks_model_indexes = list(product(range(reblock_width), range(reblock_depth), range(reblock_height)))
    list(map(lambda x: group_model_block_into_new_model(current_block_model, virtual_reblocked_model,
                                                        blocks_to_group_tuple, x), virtual_blocks_model_indexes))
    return virtual_reblocked_model


def main():
    blocks = block_model.BlockModel()

    user_input = get_user_input()

    while user_input is not '3':

        if user_input is '1':
            new_block_model = import_block_model()
            if new_block_model is not None:
                blocks = new_block_model

        elif user_input is '2':
            query_block_model(blocks)

        user_input = get_user_input()

    print("Goodbye !")


if __name__ == "__main__":
    main()
