from peewee import *


DATABASE = 'block_models.db'

database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class MineralDeposit(BaseModel):
    name = CharField(unique=True)


class BlockModel(BaseModel):
    mineral_deposit = ForeignKeyField(MineralDeposit, backref='block_models')


class Block(BaseModel):
    block_model = ForeignKeyField(BlockModel, backref='blocks')
    position_x = IntegerField()
    position_y = IntegerField()
    position_z = IntegerField()
    weight = FloatField()
    grade = FloatField()


def create_tables():
    with database:
        database.create_tables([MineralDeposit, BlockModel, Block])
