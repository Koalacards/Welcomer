from peewee import *

database = SqliteDatabase('data/data.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class WelcomeData(BaseModel):
    channel_id = IntegerField(null=True)
    guild_id = AutoField(null=True)
    role_ids = TextField(null=True)
    welcome_message = TextField(null=True)

    class Meta:
        table_name = 'WelcomeData'

