import discord
from discord.ext.commands import Cog
from discord.utils import get
from discord.ext import tasks
import logging

logger = logging.getLogger('tasks')

class FactionsCog(Cog, name = 'Factions'):
    def __init__(self, bot):
        self.__bot = bot

        self.channel_setup.start()

    @tasks.loop(hours = 168)
    async def channel_setup(self):
        await self.__bot.wait_until_ready()
        logger.info("setting up faction channels")
        for guild in self.__bot.guilds:
            factions = get(guild.categories, name="factions")
            if not factions:
                logger.info("we don't have a Community category, creating that now")
                factions = await guild.create_category("factions")

            await self.create_channel(factions, "arcanists")
            await self.create_channel(factions, "bayou")
            await self.create_channel(factions, "exporer's_society")
            await self.create_channel(factions, "guild")
            await self.create_channel(factions, "neverborn")
            await self.create_channel(factions, "resurrectionists")
            await self.create_channel(factions, "ten_thunders")


    async def create_channel(self, category:discord.CategoryChannel, channel_name:str):
        chan = get(category.text_channels, name = channel_name)
        if not chan:
            await category.create_text_channel(channel_name)
# https://discord.gg/C6AQaJcDdn