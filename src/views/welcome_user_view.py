
from discord import DMChannel, TextChannel

class WelcomeUserView():
    def __init__(self, name:str, channel:TextChannel ):
        self.__name = name
        self.__channel = channel

    async def show(self) -> None:
        await self.__channel.send("""Welcome {}! Thank you for joining us!""".format(self.__name))


class WelcomeUserDM():
    def __init__(self, name:str, direct_message:DMChannel ):
        self.__name = name
        self.__channel = direct_message

    async def show(self) -> None:
        await self.__channel.send("""Welcome {}! Thank you for joining us!
My name is Amina Naidu and I am your representative for the leagues that you can participate in.

You can find our general chat in the **Chat** channel under the **Community** category.  You will also find a place to inspire us with your models and terrain under **Hobby Inspiration** and read **Battle Reports**.

If you have ideas for channels, or how to make things better, please post them!  We're always excited for feedback.""".format(self.__name))

