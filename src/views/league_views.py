from discord import TextChannel, Embed, Message
from lib.games import Game
from views.reactions import ThumbsUpReaction, ErrorReaction, UnknownReaction

class CurrentGameView():
    def __init__(self, channel:TextChannel, game:Game):
        self.__channel = channel
        self.__game = game
        self.__message_id:str = None

    @property 
    def message_id(self):
        return self.__message_id

    async def show(self) -> None:
        if self.__game:
            e = self.__embed(self.__game)
            msg = await self.__channel.send(embed = e)
            self.__message_id = msg.id
        else:
            await self.__channel.send("There isn't a game setup for this week.")
    
    def __embed(self, game):
        return Embed(
            title = game.title,
            url = game.url,
            description = """
Click on the link above on your mobile device and then touch *Open* in the preview window.  It should take you directly to the M3e application and setup for a new game!
            """
        )

class AddGameView():
    def __init__(self, msg:Message , gameId:int):
        self.__msg = msg
        self.__gameId= gameId

    async def show(self):
        if self.__gameId:
            await self.__msg.add_reaction(ThumbsUpReaction().view())
        else:
            await self.__msg.add_reaction(UnknownReaction().view())
            await self.__msg.reply("I'm not sure why, but the message did not save.  You may want to look at how the command is used with **!help add-game**.")

class IntegrityErrorView():
    def __init__(self, msg:Message):
        self.__msg = msg

    async def show(self):
        await self.__msg.add_reaction(ErrorReaction().view())
        await self.__msg.reply("It appears that you either entered in a duplicate week or a duplicate url.  Please verify the week and a different url and try again.")

