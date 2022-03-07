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

            await self.create_channel(community, self.__announce_at)
            await self.create_channel(community, "battle_reports")
            await self.create_channel(community, "chat")
            await self.create_channel(community, "hobby_inspiration")
            await self.create_channel(community, "rules_questions")
            await self.create_channel(community, "buy-sell-trade")

    async def create_channel(self, category:discord.CategoryChannel, channel_name:str):
        chan = get(category.text_channels, name = channel_name)
        if not chan:
            await category.create_text_channel(channel_name)


# https://discord.gg/C6AQaJcDdn