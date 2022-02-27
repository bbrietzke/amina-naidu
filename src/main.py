import os, sys, logging
from discord import Intents
from lib.amina import AminaNaiduBot

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def main():
    discord_token = os.environ("DISCORD_TOKEN")
    db_path = os.environ("DB_PATH")

    intents = Intents.default()
    intents.members = True

    amina = AminaNaiduBot(
        command_prefix = '!',
        intents = intents
    )

    if db_path == None:
        print("please set the DB_PATH enviroment variable")
        sys.exit(2)

    if discord_token == None:
        print("please set the DISCORD_TOKEN enviroment variable")
        sys.exit(1)
    else:
        amina.run(discord_token)

if __name__ == '__main__':
    main()