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
                logger.info("we don't have a Community category, creating that now")
                community = await guild.create_category("Community")
                announcements = get(community.text_channels, name = "announcements")
                if not announcements:
                    await community.create_text_channel("announcements")
                reports = get(community.text_channels, name = "battle_reports")
                if not reports:
                    await community.create_text_channel("battle_reports")
                chat = get(community.text_channels, name = "chat")
                if not chat:
                    await community.create_text_channel("chat")
                rules = get(community.text_channels, name = "rules_questions")
                if not rules:
                    await community.create_text_channel("rules_questions")


# https://discord.gg/C6AQaJcDdn