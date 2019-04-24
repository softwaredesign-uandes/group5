import block_model_editor
import block_model


def test_model_reblock_empty_model():
    empty_model = block_model.BlockModel()
    reblocked_model = block_model_editor.reblock_model(empty_model, 4, 4, 4)
    assert reblocked_model.get_total_block_number() == 0, "Total block number should be 0"


def test_model_reblock_total_number():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(20, 8)
    block3 = block_model.Block(13.4, 3.7)
    block4 = block_model.Block(8.7, 2.5)
    block5 = block_model.Block(7, 5)
    block6 = block_model.Block(8, 2)
    block7 = block_model.Block(18, 15)
    block8 = block_model.Block(13, 3)
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), block1)
    blocks.add_block((0, 0, 1), block2)
    blocks.add_block((0, 1, 0), block3)
    blocks.add_block((0, 1, 1), block4)
    blocks.add_block((1, 0, 0), block5)
    blocks.add_block((1, 0, 1), block6)
    blocks.add_block((1, 1, 0), block7)
    blocks.add_block((1, 1, 1), block8)
    reblocked_model = block_model_editor.reblock_model(blocks, 2, 2, 2)
    assert reblocked_model.get_total_block_number() == 1, "Total number should be 1"


def test_model_reblock_weight():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(20, 8)
    block3 = block_model.Block(13.4, 3.7)
    block4 = block_model.Block(8.7, 2.5)
    block5 = block_model.Block(7, 5)
    block6 = block_model.Block(8, 2)
    block7 = block_model.Block(18, 15)
    block8 = block_model.Block(13, 3)
    blocks = block_model.BlockModel()
    blocks.add_block((0, 0, 0), block1)
    blocks.add_block((0, 0, 1), block2)
    blocks.add_block((0, 1, 0), block3)
    blocks.add_block((0, 1, 1), block4)
    blocks.add_block((1, 0, 0), block5)
    blocks.add_block((1, 0, 1), block6)
    blocks.add_block((1, 1, 0), block7)
    blocks.add_block((1, 1, 1), block8)
    reblocked_model = block_model_editor.reblock_model(blocks, 2, 2, 2)
    assert round(reblocked_model.get_block_at_position((0, 0, 0)).weight, 10) == 12.3625, "Weight should be 12.3625"
