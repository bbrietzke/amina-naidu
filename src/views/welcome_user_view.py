
from discord import DMChannel, TextChannel

class WelcomeUserView():
    def __init__(self, name = None, channel = TextChannel ):
        self.__name = name
        self.__channel = channel

    def show(self):
        self.__channel.send("""Welcome {}! Thank you for joining us!""".format(self.__name))


class WelcomeUserDM():
    def __init__(self, name = None, direct_message = DMChannel ):
        self.__name = name
        self.__channel = direct_message

    def show(self):
        self.__channel.send("""Welcome {}! Thank you for joining us!

        My name is Amina Naidu and I am your representative for the leagues that you can participate in.""".format(self.__name))