import block_model


def setup_blocks():
    block1 = block_model.Block(10.8)
    block1.add_mineral('Gold', 5.3)
    block2 = block_model.Block(0)
    block3 = block_model.Block(13.4)
    block3.add_mineral('Gold', 3.7)
    block3.add_mineral('Copper', 6)
    block4 = block_model.Block(8.7)
    block4.add_mineral('Gold', 2.5)
    blocks = [block1, block2, block3, block4]
    return blocks


test_blocks = setup_blocks()


def test_block_creation():
    block = test_blocks[0]
    assert block.weight == 10.8 and block.mineral_grade('Gold') == 5.3, "Weight should be 10.8 and Grade should be 5.3"


def test_block_group_add_and_count():
    block_group = block_model.BlockGroup()
    block_group.add_block(test_blocks[0])
    assert block_group.block_count() == 1, "Block count should be 1"


def test_empty_block_group_weight():
    block_group = block_model.BlockGroup()
    assert round(block_group.weight, 10) == 0, "Weight should be 0"


def test_empty_block_group_grade():
    block_group = block_model.BlockGroup()
    assert round(block_group.mineral_grade('Gold'), 10) == 0, "Grade should be 0"


def test_block_group_weight():
    block_group1 = block_model.BlockGroup()
    block_group1.add_block(test_blocks[0])
    block_group2 = block_model.BlockGroup()
    block_group2.add_block(test_blocks[2])
    block_group2.add_block(test_blocks[3])
    block_group1.add_block(block_group2)
    assert round(block_group1.weight, 10) == 32.9, "Weight should be 32.9"


def test_block_group_grade():
    block_group1 = block_model.BlockGroup()
    block_group1.add_block(test_blocks[0])
    block_group2 = block_model.BlockGroup()
    block_group2.add_block(test_blocks[2])
    block_group2.add_block(test_blocks[3])
    block_group1.add_block(block_group2)
    gold_grade = block_group1.mineral_grade('Gold')
    copper_grade = block_group1.mineral_grade('Copper')
    assert round(gold_grade, 10) == 3.9079027356 and round(copper_grade, 10) == 2.443768997, \
        "Grade should be 3.9079027356 and Copper grade should be 2.443768997"


def test_block_model_add_and_get():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    saved_block = blocks.get_block_at_position((2, 5, 8))
    same_weight = saved_block.weight == test_blocks[0].weight
    same_grade = saved_block.mineral_grade('Gold') == test_blocks[0].mineral_grade('Gold')
    assert same_weight and same_grade, "Weight and Grade should match"


def test_block_model_add_and_get_failure():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    saved_block = blocks.get_block_at_position((2, 5, 7))
    assert saved_block.weight == 0, "Block weight should be 0"


def test_block_model_get_total_blocks():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    blocks.add_block((6, 3, 9), test_blocks[2])
    assert blocks.get_total_block_number() == 2, "Total block number should be 2"


def test_block_model_get_model_dimensions():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    blocks.add_block((6, 3, 9), test_blocks[2])
    assert blocks.get_model_dimensions() == (7, 6, 10), "Model dimensions should be (7, 6, 10)"


def test_block_model_get_total_weight():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    blocks.add_block((6, 3, 9), test_blocks[1])
    blocks.add_block((1, 14, 12), test_blocks[2])
    assert round(blocks.get_total_weight(), 10) == 24.2, "Total weight should be 24.2"


def test_block_model_get_air_percentage():
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), test_blocks[0])
    blocks.add_block((0, 0, 1), test_blocks[1])
    blocks.add_block((0, 1, 0), test_blocks[2])
    blocks.add_block((0, 1, 1), test_blocks[3])
    assert blocks.get_air_percentage() == 25, "Air percentage should be 25%"


def test_block_model_get_total_mineral_grade():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    blocks.add_block((6, 3, 9), test_blocks[1])
    blocks.add_block((1, 14, 12), test_blocks[2])
    blocks.add_block((10, 14, 11), test_blocks[3])
    assert round(blocks.get_total_mineral_grade('Gold'), 10) == 11.5, "Total grade should be 11.5"


def test_block_model_get_total_grades():
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), test_blocks[0])
    blocks.add_block((6, 3, 9), test_blocks[1])
    blocks.add_block((1, 14, 12), test_blocks[2])
    blocks.add_block((10, 14, 11), test_blocks[3])
    grades = blocks.get_total_grades()
    assert round(grades['Gold'], 10) == 11.5 and grades['Copper'] == 6, \
        "Gold grade should be 11.5 and Copper grade should be 6"
