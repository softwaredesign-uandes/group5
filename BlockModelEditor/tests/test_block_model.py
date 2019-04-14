import block_model


def test_block_creation():
    block = block_model.Block(10.8, 5.3)
    assert block.weight == 10.8 and block.grade == 5.3, "Weight should be 10.8 and Grade should be 5.3"


def test_block_model_add_and_get():
    block = block_model.Block(10.8, 5.3)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block)
    saved_block = blocks.get_block_at_position((2, 5, 8))
    assert saved_block.weight == block.weight and saved_block.grade == block.grade, "Weight and Grade should match"


def test_block_model_add_and_get_failure():
    block = block_model.Block(10.8, 5.3)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block)
    saved_block = blocks.get_block_at_position((2, 5, 7))
    assert saved_block is None, "Block should be None"


def test_block_model_get_total_blocks():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(13.4, 3.7)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block1)
    blocks.add_block((6, 3, 9), block2)
    assert blocks.get_total_block_number() == 2, "Total block number should be 2"


def test_block_model_get_model_dimensions():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(13.4, 3.7)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block1)
    blocks.add_block((6, 3, 9), block2)
    assert blocks.get_model_dimensions() == (6, 5, 9), "Model dimensions should be (6, 5, 9)"


def test_block_model_get_total_weight():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(0, 0)
    block3 = block_model.Block(13.4, 3.7)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block1)
    blocks.add_block((6, 3, 9), block2)
    blocks.add_block((1, 14, 12), block3)
    assert round(blocks.get_total_weight(), 10) == 24.2, "Total weight should be 24.2"


def test_block_model_get_air_percentage():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(0, 0)
    block3 = block_model.Block(13.4, 3.7)
    block4 = block_model.Block(8.7, 2.5)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block1)
    blocks.add_block((6, 3, 9), block2)
    blocks.add_block((1, 14, 12), block3)
    blocks.add_block((10, 14, 11), block4)
    assert blocks.get_air_percentage() == 25, "Air percentage should be 25%"


def test_block_model_get_total_grade():
    block1 = block_model.Block(10.8, 5.3)
    block2 = block_model.Block(0, 0)
    block3 = block_model.Block(13.4, 3.7)
    block4 = block_model.Block(8.7, 2.5)
    blocks = block_model.BlockModel()
    blocks.add_block((2, 5, 8), block1)
    blocks.add_block((6, 3, 9), block2)
    blocks.add_block((1, 14, 12), block3)
    blocks.add_block((10, 14, 11), block4)
    assert round(blocks.get_total_grade(), 10) == 11.5, "Total grade should be 11.5"
