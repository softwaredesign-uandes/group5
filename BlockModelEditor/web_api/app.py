from flask import Flask, request, jsonify, abort, render_template
import block_model
import block_model_editor
from db.models import *

app = Flask(__name__)


@app.route('/mineral_deposits', methods=['GET', 'POST'])
def mineral_deposits_resource():
    if request.method == 'POST':
        return save_new_mineral_deposit_from_json(request.json['mineral_deposit'])
    elif request.method == 'GET':
        return convert_mineral_deposits_to_json()


@app.route('/mineral_deposits/<int:mineral_deposit_id>', methods=['GET'])
def mineral_deposit_resource(mineral_deposit_id):
    return get_mineral_deposit(mineral_deposit_id)


@app.route('/block_models', methods=['GET', 'POST'])
def block_models_resource():
    if request.method == 'POST':
        mineral_deposit_id = request.json['deposit_id']
        block_model_json = request.json['block_model']
        if 'base_block_model_id' in block_model_json:
            return reblock_model(block_model_json)
        return save_new_block_model_from_json(mineral_deposit_id, block_model_json)
    elif request.method == 'GET':
        return convert_block_models_to_json()


@app.route('/block_models/<int:block_model_id>', methods=['GET'])
def block_model_resource(block_model_id):
    return get_block_model_statistics(block_model_id)


@app.route('/block_models/<int:block_model_id>/visualize', methods=['GET'])
def block_model_resource_visualization(block_model_id):
    blocks = convert_block_model_blocks_to_json(block_model_id)
    return render_template('blocks.html', input_blocks=blocks)


@app.route('/block_models/<int:block_model_id>/blocks', methods=['GET'])
def blocks_resource(block_model_id):
    return jsonify(convert_block_model_blocks_to_json(block_model_id))


@app.route('/block_models/<int:block_model_id>/blocks/<int:flattened_block_id>', methods=['GET'])
def block_resource(block_model_id, flattened_block_id):
    converted_block_model = convert_block_model_from_database_id(block_model_id)
    dimensions_tuple = converted_block_model.get_model_dimensions()
    position_tuple = unflatten_block_id(dimensions_tuple[0], dimensions_tuple[1], flattened_block_id)
    block = converted_block_model.get_block_at_position(position_tuple)
    mineral_names = block.mineral_names
    grades = {}
    for mineral_name in mineral_names:
        grades[mineral_name] = block.mineral_grade(mineral_name)
    block_json = {'position_x': position_tuple[0], 'position_y': position_tuple[1], 'position_z': position_tuple[2],
                  'weight': block.weight, 'grades': grades}
    return jsonify(block_json)


def save_new_mineral_deposit_from_json(mineral_deposit_json):
    database.connect()
    new_mineral_deposit = MineralDeposit(name=mineral_deposit_json['name'])
    new_mineral_deposit.save()
    database.close()
    return "Mineral Deposit saved successfully."


def save_new_block_model_from_json(mineral_deposit_id, block_model_json):
    database.connect()
    new_block_model = BlockModel().create(mineral_deposit=mineral_deposit_id)
    try:
        with database.atomic():
            for i in range(len(block_model_json['x_positions'])):
                if block_model_json['x_positions'][i] == '':
                    continue
                position_x = int(block_model_json['x_positions'][i])
                position_y = int(block_model_json['y_positions'][i])
                position_z = int(block_model_json['z_positions'][i])
                weight = float(block_model_json['weights'][i])
                block = Block(position_x=position_x, position_y=position_y, position_z=position_z, weight=weight,
                              block_model=new_block_model)
                block.save()
                mineral_grades = block_model_json['grades']
                for mineral_name in mineral_grades:
                    mineral, created = Mineral.get_or_create(name=mineral_name)
                    grade = float(mineral_grades[mineral_name][i])
                    BlockMineral.create(mineral=mineral, block=block, grade=grade)
    except TypeError:
        new_block_model.delete_instance(recursive=True)
        database.close()
        abort(400)
    database.close()
    return "Block Model saved successfully."


def get_mineral_deposit(mineral_deposit_id):
    database.connect()
    mineral_deposit = MineralDeposit.get_by_id(mineral_deposit_id)
    block_models = mineral_deposit.block_models
    mineral_deposit_json = {'mineral_deposit': {'id': mineral_deposit.id, 'name': mineral_deposit.name}}
    mineral_deposit_json['mineral_deposit']['block_models'] = list(map(lambda x: {'id': x.id}, block_models))
    database.close()
    return jsonify(mineral_deposit_json)


def get_block_model_statistics(block_model_id):
    converted_block_model = convert_block_model_from_database_id(block_model_id)
    total_blocks = converted_block_model.get_total_block_number()
    total_weight = converted_block_model.get_total_weight()
    total_grades = converted_block_model.get_total_grades()
    air_percentage = converted_block_model.get_air_percentage()
    json_response = jsonify({'total_blocks': total_blocks,
                             'total_weight': total_weight,
                             'total_grades': total_grades,
                             'air_percentage': air_percentage})
    return json_response


def convert_block_model_blocks_to_json(block_model_id):
    database.connect()
    query = Block.select(Block, BlockMineral.grade, Mineral.name).where(Block.block_model_id == block_model_id) \
        .join(BlockMineral).join(Mineral)
    cursor = database.execute(query)
    block_tuples = []
    for block_tuple in cursor:
        block_tuples.append(block_tuple)
    block_ids = []
    flattened_block_ids = []
    x_positions = []
    y_positions = []
    z_positions = []
    weights = []
    grade_info = {}
    grades = {}
    for block_tuple in block_tuples:
        mineral_name = block_tuple[7]
        if mineral_name not in grades:
            grades[mineral_name] = []
    for block_tuple in block_tuples:
        block_id = block_tuple[0]
        if block_id not in block_ids:
            block_ids.append(block_id)
            x_positions.append(block_tuple[2])
            y_positions.append(block_tuple[3])
            z_positions.append(block_tuple[4])
            weights.append(block_tuple[5])
            grade_info[block_id] = {}
            for mineral_name in grades:
                grade_info[block_id][mineral_name] = 0
        grade_info[block_id][block_tuple[7]] = block_tuple[6]
    max_x = max(x_positions)
    max_y = max(y_positions)
    length = max_x + 1 if len(x_positions) != 0 else 0
    width = max_y + 1 if len(y_positions) != 0 else 0
    for block_tuple in block_tuples:
        flattened_block_ids.append(flatten_block_id(length, width, (block_tuple[2], block_tuple[3], block_tuple[4])))
    for block_id in grade_info:
        for mineral_name in grade_info[block_id]:
            grades[mineral_name].append(grade_info[block_id][mineral_name])
    database.close()
    return {'block_ids': flattened_block_ids, 'x_positions': x_positions, 'y_positions': y_positions,
            'z_positions': z_positions, 'weights': weights, 'grades': grades}


def convert_mineral_deposits_to_json():
    database.connect()
    mineral_deposits = MineralDeposit.select()
    mineral_deposits_json = {'mineral_deposits': list(map(lambda x: {'id': x.id, 'name': x.name}, mineral_deposits))}
    database.close()
    return jsonify(mineral_deposits_json)


def convert_block_models_to_json():
    database.connect()
    mineral_deposits = MineralDeposit.select()
    mineral_deposits_json = {}
    for deposit in mineral_deposits:
        block_models = BlockModel.select().where(BlockModel.mineral_deposit == deposit)
        mineral_deposits_json[deposit.name] = {'block_models': list(map(lambda x: {'id': x.id}, block_models))}
    database.close()
    return jsonify({'mineral_deposits': mineral_deposits_json})


def convert_block_model_from_database_id(block_model_id):
    database.connect()
    query = Block.select(Block, BlockMineral.grade, Mineral.name).where(Block.block_model_id == block_model_id)\
        .join(BlockMineral).join(Mineral)
    cursor = database.execute(query)
    converted_block_model = block_model.BlockModel()
    list(map(lambda x: add_to_block_model_from_database_block(converted_block_model, x), cursor))
    database.close()
    return converted_block_model


def add_to_block_model_from_database_block(block_model_to_add, database_block_tuple):
    position_x = database_block_tuple[2]
    position_y = database_block_tuple[3]
    position_z = database_block_tuple[4]
    weight = database_block_tuple[5]
    grade = database_block_tuple[6]
    mineral_name = database_block_tuple[7]
    position_tuple = (position_x, position_y, position_z)
    if position_tuple in block_model_to_add.blocks:
        block_model_to_add.blocks[position_tuple].add_mineral(mineral_name, grade)
    else:
        converted_block = block_model.Block(weight)
        converted_block.add_mineral(mineral_name, grade)
        block_model_to_add.add_block(position_tuple, converted_block)


def save_to_database_from_block_model_object(block_model_object):
    database.connect()
    new_block_model = BlockModel().create()
    for position_tuple in block_model_object.blocks:
        position_x = position_tuple[0]
        position_y = position_tuple[1]
        position_z = position_tuple[1]
        weight = block_model_object[position_tuple].weight
        block = Block(position_x=position_x, position_y=position_y, position_z=position_z, weight=weight,
                      block_model=new_block_model)
        block.save()
        mineral_names = block_model_object[position_tuple].mineral_names
        for mineral_name in mineral_names:
            mineral, created = Mineral.get_or_create(name=mineral_name)
            grade = block_model_object[position_tuple].mineral_grade(mineral_name)
            BlockMineral.create(mineral=mineral, block=block, grade=grade)
    database.close()


def reblock_model(block_model_to_reblock_json):
    block_model_id = int(block_model_to_reblock_json['base_block_model_id'])
    blocks_to_group_tuple = (int(block_model_to_reblock_json['rx']), int(block_model_to_reblock_json['ry']),
                             int(block_model_to_reblock_json['rz']))
    converted_block_model = convert_block_model_from_database_id(block_model_id)
    reblocked_model = block_model_editor.virtual_reblock_model(converted_block_model, blocks_to_group_tuple)
    save_to_database_from_block_model_object(reblocked_model)


def flatten_block_id(model_length, model_width, position_tuple):
    flattened_id = position_tuple[2] * model_length * model_width + position_tuple[1] * model_length + position_tuple[0]
    return flattened_id


def unflatten_block_id(model_length, model_width, block_id):
    position_z = block_id // (model_length * model_width)
    block_id -= position_z * model_length * model_width
    position_y = block_id // model_length
    position_x = block_id % model_length
    return position_x, position_y, position_z
