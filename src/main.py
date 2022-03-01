import os, sys, logging
from discord import Intents
import sqlite3
from lib.amina import AminaNaiduBot
from startup_tasks import StartupTasks
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


def main():
    discord_token = os.environ.get("DISCORD_TOKEN")
    db_path = os.environ.get("DB_PATH")

    intents = Intents.default()
    intents.members = True

    amina = AminaNaiduBot(
        command_prefix = '!',
        intents = intents
    )

    if db_path == None:
        print("please set the DB_PATH enviroment variable")
        sys.exit(2)
    else:
        with DatabaseService(db_path) as cursor:
            (q, _) = DatabaseService.database_ddl()
            cursor.executescript(q)

        amina.add_cog(StartupTasks(amina, db_path))

    if discord_token == None:
        print("please set the DISCORD_TOKEN enviroment variable")
        sys.exit(1)
    else:
        amina.run(discord_token)

    
    sys.exit(3)

if __name__ == '__main__':
    main()