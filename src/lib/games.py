
from lib.constants import SELECT_CURRENT_GAME, INSERT_GAME, UPDATE_GAME, SELECT_CURRENT_GAME_NULL_MESSAGE

class Game():
    def __init__(self, id:int, url:str = None, message_id:str = None, title:str = None, start_week:str = None):
        self.__id = id
        self.__url = url
        self.__message_id = message_id
        self.__title = title
        self.__start_week = start_week

    @property
    def id(self) -> int:
        return self.__id

    @property
    def url(self) -> str:
        return self.__url

    @property
    def message_id(self) -> str:
        return self.__message_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def start_week(self) -> int:
        return self.__start_week

    @message_id.setter
    def message_id(self, message_id):
        self.__message_id = message_id

    def save(self):
        if self.__id:
            return (
                UPDATE_GAME,
                (self.__url, self.__title, self.__start_week, self.__message_id, self.__id,)
            )
        else:
            return (
                INSERT_GAME,
                (self.__url, self.__title, self.__start_week,)
            )

    @staticmethod
    def find_by_week(week):
        return (
            SELECT_CURRENT_GAME,
            ( week, )
        )

    @staticmethod
    def find_by_week_without_message_id(week):
        return (
            SELECT_CURRENT_GAME_NULL_MESSAGE,
            ( week, )
        )

    @staticmethod
    def find_by_message_id(message_id):
        return (
            "",
            ( message_id, )
        )