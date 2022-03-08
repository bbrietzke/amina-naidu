
from lib.constants import SELECT_CURRENT_GAME

class Game():
    def __init__(self, id:int, url:str = None, message_id:str = None, title:str = None, start_week:str = None):
        self.__id = id
        self.__url = url
        self.__message_id = message_id
        self.__title = title
        self.__start_week = start_week

    @property
    def id(self):
        return self.__id

    @property
    def url(self):
        return self.__url

    @property
    def message_id(self):
        return self.__message_id

    @property
    def title(self):
        return self.__title

    @property
    def start_week(self):
        return self.__start_week

    @message_id.setter
    def message_id(self, message_id):
        self.__message_id = message_id

    def save(self):
        if self.__id:
            pass
        else:
            pass

    @staticmethod
    def find_by_week(week):
        return (
            SELECT_CURRENT_GAME,
            ( week, )
        )

    def find_by_message_id(message_id):
        return (
            "",
            ( message_id, )
        )