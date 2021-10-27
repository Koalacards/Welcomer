from data import WelcomeData
from peewee import *

def set_channel_id(guild_id:int, channel_id:int):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        WelcomeData.create(guild_id=guild_id, channel_id=channel_id, role_ids='[]', welcome_message="")
    else:
        new_query = WelcomeData.update(channel_id=channel_id).where(WelcomeData.guild_id==guild_id)
        return new_query.execute()

def get_channel_id(guild_id:int):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.channel_id

def set_role_ids(guild_id:int, role_ids:str):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        WelcomeData.create(guild_id=guild_id, channel_id=0, role_ids=role_ids, welcome_message="")
    else:
        new_query = WelcomeData.update(role_ids=role_ids).where(WelcomeData.guild_id==guild_id)
        return new_query.execute()
    
def get_role_ids(guild_id:int):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.role_ids

def set_welcome_message(guild_id:int, welcome_message:str):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        WelcomeData.create(guild_id=guild_id, channel_id=0, role_ids='[]', welcome_message=welcome_message)
    else:
        new_query = WelcomeData.update(welcome_message=welcome_message).where(WelcomeData.guild_id==guild_id)
        return new_query.execute()

def get_welcome_message(guild_id:int):
    query = WelcomeData.select().where(WelcomeData.guild_id==guild_id)
    if len(query) == 0:
        return None
    else:
        for item in query:
            return item.welcome_message