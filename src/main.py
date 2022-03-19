import os, sys, logging
from discord import Intents
from lib.amina import AminaNaiduBot
from lib.constants import ANNOUNCEMENTS_CHANNEL_NAME
from player_cog import PlayerCog
from community_cog import CommunityCog
from faction_cog import FactionsCog
from league_cog import LeagueCog
from rss_cog import RSSCog
from lib.database_service import DatabaseService

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger2 = logging.getLogger('amina')
logger2.setLevel(logging.DEBUG)
handler2 = logging.StreamHandler(sys.stdout)
handler2.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger2.addHandler(handler2)

logger3 = logging.getLogger('tasks')
logger3.setLevel(logging.DEBUG)
handler3 = logging.StreamHandler(sys.stdout)
handler3.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger3.addHandler(handler3)

logger4 = logging.getLogger('league')
logger4.setLevel(logging.DEBUG)
handler4 = logging.StreamHandler(sys.stdout)
handler4.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger4.addHandler(handler4)

logger5 = logging.getLogger('rss')
logger5.setLevel(logging.DEBUG)
handler5 = logging.StreamHandler(sys.stdout)
handler5.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger5.addHandler(handler5)


def main():
    discord_token = os.environ.get("DISCORD_TOKEN")
    db_path = os.environ.get("DB_PATH")
    mysql = os.environ.get("MYSQL")

    intents = Intents.default()
    intents.members = True

    amina = AminaNaiduBot(
        command_prefix = '!',
        intents = intents
    )

    amina.add_cog(CommunityCog(amina, ANNOUNCEMENTS_CHANNEL_NAME))
    amina.add_cog(FactionsCog(amina))

    if db_path != None:
        with DatabaseService(db_path) as cursor:
            script = DatabaseService.database_ddl()
            cursor.executescript(script)

        amina.add_cog(PlayerCog(amina, DatabaseService(db_path)))
        amina.add_cog(LeagueCog(amina, DatabaseService(db_path), announcements_channel = "amina_testing"))
        amina.add_cog(RSSCog(amina, DatabaseService(db_path), announcements_channel = ANNOUNCEMENTS_CHANNEL_NAME))
    elif mysql != None:
        pass
    else:
        print("please set the DB_PATH or MYSQL enviroment variable")

    if discord_token == None:
        print("please set the DISCORD_TOKEN enviroment variable")
        sys.exit(1)
    else:
        amina.run(discord_token)

if __name__ == '__main__':
    main()