
from lib.constants import INSERT_PLAYER, UPDATE_PLAYER_BY_ID, SELECT_PLAYER_BY_DISCORD

class Player():
    def __init__(self, id:int, discord_id:str = None, name:str = None):
        self.__id = id
        self.__discord_id = discord_id
        self.__name = name
    
    @property
    def name(self):
        return self.__name

    @property
    def discord_id(self):
        return self.__discord_id

    @property
    def id(self):
        return self.__id

    def save(self):
        if self.__id:
            return (
                UPDATE_PLAYER_BY_ID, 
                (self.__name, self.__id,)
            )
        else: 
            return (
                INSERT_PLAYER, 
                (self.__discord_id, self.__name,)
            )

    @staticmethod
    def find_by_discord_id(discord_id):
        return (
            SELECT_PLAYER_BY_DISCORD,
            (discord_id,)
        )