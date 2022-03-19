import discord
from discord import Message, Embed, TextChannel
from discord.ext.commands import Cog
from discord.ext import commands, tasks
from discord.utils import get
import logging
from sqlite3 import IntegrityError

from lib.rss_manager import RSSManager
from views.reactions import ThumbsUpReaction, ErrorReaction, UnknownReaction

logger = logging.getLogger('rss')

class IntegrityErrorView():
    def __init__(self, msg:Message):
        self.__msg = msg

    async def show(self):
        await self.__msg.add_reaction(ErrorReaction().view())
        await self.__msg.reply("It appears that you either entered in a duplicate week or a duplicate url.  Please verify the week and a different url and try again.")

class EntryView():
    def __init__(self, ctx:TextChannel, url:str, title:str, feed_title:str):
        self.__ctx = ctx
        self.__url = url
        self.__title = title
        self.__feed_title = feed_title
        self.__message_id = 0

    @property
    def id(self):
        return self.__message_id

    async def show(self):
        e = self.__embed()
        r = await self.__ctx.send(embed = e)
        self.__message_id = r.id

        return self

    def __embed(self):
        return Embed(
            title = self.__title,
            url =  self.__url,
            description = "Read the lastest from {}".format(self.__feed_title)
        )

class AddFeedView():
    def __init__(self, msg:Message , id:int):
        self.__msg = msg
        self.__id= id

    async def show(self):
        if self.__id:
            await self.__msg.add_reaction(ThumbsUpReaction().view())
        else:
            await self.__msg.add_reaction(UnknownReaction().view())
            await self.__msg.reply("I'm not sure why, but the command did not execute properly.  You may want to look at how the command is used with **!help add-game**.")


class RSSCog(Cog, name = "RSS Commands"):
    def __init__(self, bot, service_manager, announcements_channel = None):
        self.__service = service_manager
        self.__announcements = announcements_channel
        self.__bot = bot
        self.check_feeds.start()

    @tasks.loop(minutes=120, hours=0, seconds=0, loop = None)
    async def check_feeds(self):
        if self.__announcements:
            channel = None
            updated = []
            for guild in self.__bot.guilds:
                channel = get(guild.text_channels, name = self.__announcements)
            
            boss = RSSManager(self.__service)
            new_entries = boss.new_entries()

            logger.debug("{} entries need to be published".format(len(new_entries)))

            for entry in new_entries:
                e = EntryView(channel, entry.url, entry.title, entry.feed_title)
                await e.show()
                updated.append((e.id, entry.url))

            await boss.published_entries(updated)


    @check_feeds.before_loop
    async def before_check_feeds(self):
       await self.__bot.wait_until_ready()

    @commands.is_owner()
    @commands.command(name = "add-feed", usage = "url", brief = "Adds and refreshes a new RSS feed.  Will not print any items from the current feed, instead any new items will be printed.")
    async def add_feed(self, ctx, url):
        try:
            boss = RSSManager(self.__service)
            results = boss.add_feed(url)
            logger.info(results)
            await AddFeedView(ctx.message, results).show()
        except IntegrityError as error:
            await IntegrityErrorView(ctx.message).show()