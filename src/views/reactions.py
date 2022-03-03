import discord

class ThumbsUpReaction():
    def __init__(self):
        pass

    def view(self) -> discord.Emoji:
        return '👍'

class ErrorReaction():
    def __init__(self):
        pass

    def view(self) -> discord.Emoji:
        return '❌'

class UnknownReaction():
    def __init__(self):
        pass

    def view(self) -> discord.Emoji:
        return '🤦'