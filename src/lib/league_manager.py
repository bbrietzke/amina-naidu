from lib.player import Player

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

