import block_model_editor
import block_model


def setup_blocks():
    block1 = block_model.Block(10.8)
    block1.add_mineral('Gold', 5.3)
    block1.add_mineral('Copper', 4.2)
    block2 = block_model.Block(20)
    block2.add_mineral('Gold', 8)
    block2.add_mineral('Copper', 3)
    block3 = block_model.Block(13.4)
    block3.add_mineral('Gold', 3.7)
    block4 = block_model.Block(8.7)
    block4.add_mineral('Gold', 2.5)
    block1.add_mineral('Copper', 5)
    block5 = block_model.Block(7)
    block5.add_mineral('Gold', 5)
    block6 = block_model.Block(8)
    block6.add_mineral('Gold', 2)
    block7 = block_model.Block(18)
    block7.add_mineral('Gold', 15)
    block8 = block_model.Block(13)
    block8.add_mineral('Gold', 3)
    blocks = [block1, block2, block3, block4, block5, block6, block7, block8]
    return blocks


test_blocks = setup_blocks()


def test_model_virtual_reblock_empty_model():
    empty_model = block_model.BlockModel()
    reblocked_model = block_model_editor.virtual_reblock_model(empty_model, (4, 4, 4))
    assert reblocked_model.get_total_block_number() == 0, "Total block number should be 0"


def test_model_virtual_reblock_total_number():
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), test_blocks[0])
    blocks.add_block((0, 0, 1), test_blocks[1])
    blocks.add_block((0, 1, 0), test_blocks[2])
    blocks.add_block((0, 1, 1), test_blocks[3])
    blocks.add_block((1, 0, 0), test_blocks[4])
    blocks.add_block((1, 0, 1), test_blocks[5])
    blocks.add_block((1, 1, 0), test_blocks[6])
    blocks.add_block((1, 1, 1), test_blocks[7])
    reblocked_model = block_model_editor.virtual_reblock_model(blocks, (2, 2, 2))
    assert reblocked_model.get_total_block_number() == 1, "Total number should be 1"


def test_model_virtual_reblock_not_divisible_by_factor_total_number():
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), test_blocks[0])
    blocks.add_block((0, 0, 1), test_blocks[1])
    blocks.add_block((0, 1, 0), test_blocks[2])
    blocks.add_block((0, 1, 1), test_blocks[3])
    reblocked_model = block_model_editor.virtual_reblock_model(blocks, (2, 2, 2))
    assert reblocked_model.get_total_block_number() == 1, "Total number should be 1"


def test_model_virtual_reblock_weight():
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), test_blocks[0])
    blocks.add_block((0, 0, 1), test_blocks[1])
    blocks.add_block((0, 1, 0), test_blocks[2])
    blocks.add_block((0, 1, 1), test_blocks[3])
    blocks.add_block((1, 0, 0), test_blocks[4])
    blocks.add_block((1, 0, 1), test_blocks[5])
    blocks.add_block((1, 1, 0), test_blocks[6])
    blocks.add_block((1, 1, 1), test_blocks[7])
    reblocked_model = block_model_editor.virtual_reblock_model(blocks, (2, 2, 2))
    assert round(reblocked_model.get_block_at_position((0, 0, 0)).weight, 10) == 98.9, "Weight should be 98.9"


def test_model_virtual_reblock_grade():
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), test_blocks[0])
    blocks.add_block((0, 0, 1), test_blocks[1])
    blocks.add_block((0, 1, 0), test_blocks[2])
    blocks.add_block((0, 1, 1), test_blocks[3])
    blocks.add_block((1, 0, 0), test_blocks[4])
    blocks.add_block((1, 0, 1), test_blocks[5])
    blocks.add_block((1, 1, 0), test_blocks[6])
    blocks.add_block((1, 1, 1), test_blocks[7])
    reblocked_model = block_model_editor.virtual_reblock_model(blocks, (2, 2, 2))
    gold_grade = reblocked_model.get_block_at_position((0, 0, 0)).mineral_grade('Gold')
    copper_grade = reblocked_model.get_block_at_position((0, 0, 0)).mineral_grade('Copper')
    assert round(gold_grade, 10) == 6.5578361982 and round(copper_grade, 10) == 1.1526794742, \
        "Gold grade should be 6.5578361982 and Copper grade should be 1.1526794742"
