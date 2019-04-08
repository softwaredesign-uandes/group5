from pathlib import Path
import block_model


def import_block_model_from_zuck_file(filename):
    new_blocks = []
    if Path(filename).is_file():
        source_file = open(filename, "r")
        file_lines = source_file.readlines()

        for line in file_lines:
            
            block_values = line.split(' ')

            #weight = float(block_values[0])
            
            new_blocks.append(block_values)

    return new_blocks


def get_user_input():
    print("\n[1] Import new Block Model")
    print("[2] Query current Block Model.")
    print("[3] Quit.")

    return input("\nChoose a command: ")

def get_user_query():
    print("\nWhich information you want from the loaded model?")
    print("")
    print("[1] Number of blocks.")
    print("[2] Total weight of the Mineral Deposit.")
    print("[3] Percentage of Air blocks (blocks with weight 0).")
    print("[4] Total mineral weight for all minerals in the Mineral Deposit")
    print("[5] Go Back.")

    return input("\nChoose a command: ")

    


blocks = []

user_input = get_user_input()

while user_input is not 3:

    if user_input is 1:
        print("Please indicate in which columns are the following data placed (spaced separated)")
        print("TOTAL WEIGHT|MINERAL 1 WEIGHT|MINERAL 2 WEIGHT|...")
        data = [int(x) for x in raw_input().split()]
        data[:] = [x - 1 for x in data]
        weight = data[0]

        input_filename = input("Please insert the source file name: ")

        imported_blocks = import_block_model_from_zuck_file(input_filename)
        
        if len(imported_blocks) == 0:
            print("Error importing Block Model.")
        else:
            blocks = imported_blocks
            print("Block Model imported successfully.")


    elif user_input is 2:
        query = get_user_query()
        while query is not 5:
            if query is 1:
                print(len(imported_blocks))
                
            elif query is 2:
                Total_weight = 0
                for i in imported_blocks:
                    Total_weight += float(i[weight])
                print(Total_weight)
            elif query is 3:
                zeros = 0
                for i in imported_blocks:
                    if i[weight] == 0:
                        zeros += 1
                if zeros == 0:
                    print(zeros)
                else:
                    print(len(imported_blocks)/zeros)
            elif query is 4:
                Total_weight_minerals = 0
                for i in imported_blocks:
                    for j in data[0:]:
                        Total_weight_minerals += float(i[j])
                print(Total_weight_minerals) 

            query = get_user_query()


    user_input = get_user_input()

print("Goodbye !")
    