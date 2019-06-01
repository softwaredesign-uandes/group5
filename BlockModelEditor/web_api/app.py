from flask import Flask, request, jsonify, abort
import block_model
import block_model_editor

app = Flask(__name__)


class MineralDepositContainer:
    def __init__(self):
        self.mineral_deposits = []


class BlockModelContainer:
    def __init__(self):
        self.loaded_block_model = block_model.BlockModel()

    def set_block_model(self, new_block_model):
        self.loaded_block_model = new_block_model


block_model_container = BlockModelContainer()


@app.route('/block_model', methods=['GET', 'POST'])
def block_model_resource():
    if request.method == 'POST':
        return load_block_model(request.json['block_model'])
    elif request.method == 'GET':
        return get_block_model_statistics()


@app.route('/block_model/reblocked_model', methods=['POST'])
def get_reblocked_model():
    request_body = request.json
    if request_body is None:
        abort(400)
    blocks_to_group_tuple = (int(request_body['rx']), int(request_body['ry']), int(request_body['rz']))
    reblocked_model = block_model_editor.reblock_model(block_model_container.loaded_block_model, blocks_to_group_tuple)
    json_response = convert_block_model_to_json(reblocked_model)
    return json_response


def load_block_model(block_model_json):
    new_block_model = block_model_editor.import_block_model_from_json_object(block_model_json)
    if new_block_model is None:
        abort(400)
    block_model_container.set_block_model(new_block_model)
    return "Block Model loaded successfully."


def get_block_model_statistics():
    total_blocks = block_model_container.loaded_block_model.get_total_block_number()
    total_weight = block_model_container.loaded_block_model.get_total_weight()
    total_grade = block_model_container.loaded_block_model.get_total_grade()
    air_percentage = block_model_container.loaded_block_model.get_air_percentage()
    json_response = jsonify({'total_blocks': total_blocks,
                             'total_weight': total_weight,
                             'total_grade': total_grade,
                             'air_percentage': air_percentage})
    return json_response


def convert_block_model_to_json(block_model_to_convert):
    x_positions = []
    y_positions = []
    z_positions = []
    weights = []
    grades = []
    for position, block in block_model_to_convert.blocks.items():
        x_positions.append(position[0])
        y_positions.append(position[1])
        z_positions.append(position[2])
        weights.append(block.weight)
        grades.append(block.grade)
    return jsonify({'x_positions': x_positions,
                    'y_positions': y_positions,
                    'z_positions': z_positions,
                    'weights': weights,
                    'grades': grades})
