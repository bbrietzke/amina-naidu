from discord.ext.commands import Cog
from discord.ext import tasks
import logging

logger = logging.getLogger('amina')

class StartupTasks(Cog, name = 'Startup Tasks'):
    def __init__(self, bot, db):
        self.__bot = bot
        self.__db = db

        self.players.start()
        self.channel_setup.start()
        self.role_setup.start()

    @tasks.loop(hours = 12)
    async def players(self):
        await self.__bot.wait_until_ready()
        logger.info("starting to setup players")
        

    @tasks.loop(hours = 168)
    async def role_setup(self):
        await self.__bot.wait_until_ready()
        logger.info("starting to setup roles")

    @tasks.loop(hours = 168)
    async def channel_setup(self):
        await self.__bot.wait_until_ready()
        logger.info("starting to setup channels")