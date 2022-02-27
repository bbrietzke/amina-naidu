from discord.ext.commands import Bot
import logging

logger = logging.getLogger('amina')

class AminaNaiduBot(Bot):
    async def on_ready(self):
        logger.info("* * * * * * AminaNaiduBot is up and running * * * * * *")
