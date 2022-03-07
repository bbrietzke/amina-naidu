from discord.ext.commands import Cog
from discord.utils import get
from discord.ext import tasks
import logging

logger = logging.getLogger('tasks')

class StartupTasks(Cog, name = 'Startup Tasks'):
    def __init__(self, bot, service_manager):
        self.__bot = bot
        self.__service = service_manager

        self.channel_setup.start()

    @tasks.loop(hours = 168)
    async def channel_setup(self):
        await self.__bot.wait_until_ready()
        logger.info("setting up channels")
        for guild in self.__bot.guilds:
            community = get(guild.categories, name="Community")
            if not community:
                logger.info("we don't have a Community channel, creating that now")
                community = await guild.create_category("Community")
                announcements = get(community.text_channels, name = "announcements")
                if not announcements:
                    await community.create_text_channel("announcements")