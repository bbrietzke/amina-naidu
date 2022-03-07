from discord.ext.commands import Cog
from discord.utils import get
from discord.ext import tasks
import logging

logger = logging.getLogger('tasks')

class StartupTasks(Cog, name = 'Startup Tasks'):
    def __init__(self, bot):
        self.__bot = bot


# https://discord.gg/C6AQaJcDdn