from pathlib import Path
import block_model


def import_block_model_from_zuck_file(filename):
    new_blocks = []
    if Path(filename).is_file():
        source_file = open(filename, "r")
        file_lines = source_file.readlines()

        for line in file_lines:
            block_values = line.split(' ')
            if len(block_values) == 8:
                position_x = int(block_values[1])
                position_y = int(block_values[2])
                position_z = int(block_values[3])
                weight = float(block_values[6])
                grade = float(block_values[7])
                new_blocks.append(block_model.Block(position_x, position_y, position_z, weight, grade))

    return new_blocks


def get_user_input():
    print("\n[1] Import new Block Model (Zuck .blocks format).")
    # print("[2] Query current Block Model.")
    print("[q] Quit.")

    return input("\nChoose a command: ")


blocks = []
user_input = get_user_input()
while user_input is not 'q':

    if user_input is '1':
        input_filename = input("Please insert the source file name: ")
        imported_blocks = import_block_model_from_zuck_file(input_filename)
        if len(imported_blocks) == 0:
            print("Error importing Block Model.")
        else:
            blocks = imported_blocks
            print("Block Model imported successfully.")

    user_input = get_user_input()
