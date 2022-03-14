import discord
from discord.ext.commands import Cog
from discord.ext import tasks
from discord.utils import get
from lib.league_manager import LeagueManager
from views.welcome_user_view import WelcomeUserView, WelcomeUserDM
import logging

logger = logging.getLogger('tasks')

class PlayerCog(Cog, name = "Player Cog"):
    def __init__(self, bot, service_manager):
        self.__bot = bot
        self.__service = service_manager
        self.players.start()

    @Cog.listener()
    async def on_member_join(self, member:discord.Member):
        logger.info("a new member has joined!")
        with LeagueManager(self.__service) as lm:
            lm.save_player(0, discord_id=member.id, name = member.display_name)
            logger.info("new member {}!".format(member.display_name))

        dm = await member.create_dm()

        if dm is None:
            general = get(self.__bot.guild.text_channels, name="general")
            if not general:
                await WelcomeUserView(member.display_name, general).show()
                logger.info("messaged {} on the general chat".format(member.display_name))
            else:
                logger.info("no general channel? what's up with that?")
        else:
            await WelcomeUserDM(member.display_name, dm).show()
            logger.info("DMed {}".format(member.display_name))

    @tasks.loop(minutes=720, hours=0, seconds=0, loop = None)
    async def players(self):
        logger.info("starting to setup players")
        cnt = 0
        models = []
        
        for member in self.__bot.get_all_members():
            cnt = cnt + 1
            models.append((member.id, member.display_name,))

        with LeagueManager(self.__service) as lm:
            lm.save_players(models)

        logger.info("added or updated {} members".format(len(models)))

    @players.before_loop
    async def before_players(self):
       await self.__bot.wait_until_ready()