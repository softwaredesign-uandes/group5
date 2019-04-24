from pathlib import Path
import block_model


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


def reblock_blocks_into_one(current_block_model, starting_position_tuple, blocks_to_group_x, blocks_to_group_y,
                            blocks_to_group_z):
    total_weight = 0
    starting_x, starting_y, starting_z = starting_position_tuple
    for i in range(blocks_to_group_x):
        for j in range(blocks_to_group_y):
            for k in range(blocks_to_group_z):
                block = current_block_model.get_block_at_position((starting_x + i, starting_y + j, starting_z + k))
                if block is not None:
                    total_weight += block.weight
    return block_model.Block(total_weight, 0)


def reblock_model(current_block_model, blocks_to_group_x, blocks_to_group_y, blocks_to_group_z):
    width, depth, height = current_block_model.get_model_dimensions()
    reblock_width = int(width / blocks_to_group_x)
    reblock_depth = int(depth / blocks_to_group_y)
    reblock_height = int(height / blocks_to_group_z)
    reblocked_model = block_model.BlockModel()
    for i in range(reblock_width):
        for j in range(reblock_depth):
            for k in range(reblock_height):
                starting_block_position = (i * blocks_to_group_x, j * blocks_to_group_y, k * blocks_to_group_z)
                reblocked_block = reblock_blocks_into_one(current_block_model, starting_block_position,
                                                          blocks_to_group_x, blocks_to_group_y, blocks_to_group_z )
                reblocked_model.add_block((i, j, k), reblocked_block)
    return reblocked_model


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