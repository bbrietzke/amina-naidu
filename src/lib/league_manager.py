from datetime import date
from email import message
import logging

from lib.player import Player
from lib.games import Game

logger = logging.getLogger("league")

class LeagueManager():
    def __init__(self, service_manager):
        self.__service = service_manager

    def __enter__(self):
        return LeagueManagerInner(self.__service)

    def __exit__(self, type, value, traceback):
        pass

class LeagueManagerInner():
    def __init__(self, service_manager):
        self.__service = service_manager

    def save_player(self, id:int, discord_id:str = None, name:str = None):
        player = Player(id, discord_id=discord_id, name = name)
        with self.__service as c:
            (q, p) = player.save()
            c.execute(q, p)

    def save_players(self, models:list):
        player = Player(0)
        with self.__service as c:
            (q, _) = player.save()
            c.executemany(q, models)

    def save_game(self, id:int, message_id:str = None, url:str = None, title:str = None, start_week = None):
        game = Game(id, url = url, message_id = message_id, title = title, start_week = start_week)
        (q, p) = game.save()
        with self.__service as c:
            r = c.execute(q, p)
            return r.lastrowid

    def show_current_game(self):
        this_week:int = date.today().isocalendar().week
        (q, p) = Game.find_by_week(this_week)
        with self.__service as c:
            retVal = c.execute(q, p).fetchone()
            if retVal:
                (id, url, title, start_week, message_id) = retVal
                return Game(id, url = url, title = title, start_week = start_week, message_id = message_id)
            else:
                return None
             
