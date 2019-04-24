import block_model_editor
import block_model


def test_model_reblock_empty_model():
    empty_model = block_model.BlockModel()
    reblocked_model = block_model_editor.reblock_model(empty_model, 4, 4, 4)
    assert reblocked_model.get_total_block_number() == 0, "Total block number should be 0"
