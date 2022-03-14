import discord
from sqlite3 import IntegrityError
from datetime import datetime
from discord.ext.commands import Cog
from discord.ext import commands, tasks
from discord.utils import get
from lib.league_manager import LeagueManager
from views.league_views import CurrentGameView, AddGameView, IntegrityErrorView
from views.reactions import ThumbsUpReaction, ErrorReaction, UnknownReaction
import logging

logger = logging.getLogger('league')

class LeagueCog(Cog, name = "League Commands"):
    def __init__(self, bot, service_manager, announcements_channel = None):
        self.__service = service_manager
        self.__announcements = announcements_channel
        self.__bot = bot
        self.announce_current_game.start()

    @commands.is_owner()
    @commands.command(name = "add-game", usage = "YYYY/MM/DD http://example.me \"Description goes here\"", brief = "Adds a league game for a specific week to the system.")
    async def add_game(self, ctx, week_of:str, url: str, description: str):
        _date:str = datetime.strptime(week_of, '%Y/%m/%d').isocalendar().week

        try:
             with LeagueManager(self.__service) as lm:
                r = lm.save_game(0, url = url, title = description, start_week = _date)

                await AddGameView(ctx.message, r).show()
        except IntegrityError as error:
            await IntegrityErrorView(ctx.message).show()

    @commands.command(name = "show-game", brief = "Shows the current game for this week")
    async def show_game(self, ctx):
        game = await self.show_current_game()

        await CurrentGameView(ctx.message.channel, game).show()

    @commands.command(name = "join-league", brief = "Join the league with a specific faction provided with the command", usage = "faction (a|b|es|g|nb|o|r|10t)")
    async def join_league(self, ctx):
        pass

    @tasks.loop(minutes=240, hours=0, seconds=0, loop = None)
    async def announce_current_game(self):
        logger.info("starting announce_current_game")
        _date:str = datetime.today().isocalendar().week

    @announce_current_game.before_loop
    async def before_announce_current_game(self):
       await self.__bot.wait_until_ready()

    async def show_current_game(self):
        with LeagueManager(self.__service) as lm:
            return lm.show_current_game()

