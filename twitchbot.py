import logging, os, curses, threading, sys
from dotenv import load_dotenv
from emoji import demojize
from twitchio.ext import commands
from twitchio import client
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Bot(commands.Bot):

    def __init__(self, channels):
        super().__init__(
            token=os.getenv('TOKEN'),
            client_id=os.getenv('CLIENT_ID'),
            nick=os.getenv('NICKNAME'),
            prefix='>',
        )
        initial_channels=channels
        sys.tracebacklimit = 0

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        if len(self.initial_channels) == 1: print('<'+message.author.name+'> '+demojize(message.content))
        else: print('['+message.channel.name+'] <'+message.author.name+'> '+demojize(message.content))
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

class curses_Bot(commands.Bot):

    def __init__(self, channels):
        self.chatlog = []
        super().__init__(
            irc_token=os.getenv('TOKEN'),
            client_id=os.getenv('CLIENT_ID'),
            nick=os.getenv('NICKNAME'),
            prefix='>',
            initial_channels=channels
        )

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        if len(self.initial_channels) == 1: self.chatlog.append('<'+message.author.name+'> '+demojize(message.content))
        else: self.chatlog.append('['+message.channel.name+'] <'+message.author.name+'> '+demojize(message.content))
        print(bot.chatlog[len(bot.chatlog)-1])
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


if __name__ == '__main__':
    bot = Bot(['AnonymousCrow', 'eggdotpng'])
    bot.run()
