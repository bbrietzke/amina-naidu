import discord
from discord.ext.commands import Cog
from discord.utils import get
from discord.ext import tasks
import logging

logger = logging.getLogger('tasks')

class CommunityCog(Cog, name = 'Community'):
    def __init__(self, bot, announcments:str):
        self.__bot = bot
        self.__announce_at = announcments

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
                announcements = get(community.text_channels, name = self.__announce_at)
                if not announcements:
                    await community.create_text_channel(self.__announce_at)
                reports = get(community.text_channels, name = "battle_reports")
                if not reports:
                    await community.create_text_channel("battle_reports")
                chat = get(community.text_channels, name = "chat")
                if not chat:
                    await community.create_text_channel("chat")
                rules = get(community.text_channels, name = "rules_questions")
                if not rules:
                    await community.create_text_channel("rules_questions")

    async def create_channel(self, category:discord.CategoryChannel, channel_name:str):
        chan = get(category.text_channels, name = channel_name)
        if not chan:
            await category.create_text_channel(channel_name)


# https://discord.gg/C6AQaJcDdn