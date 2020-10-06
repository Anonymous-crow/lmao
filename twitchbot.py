import os
from dotenv import load_dotenv
from emoji import demojize
from twitchio.ext import commands
from twitchio import client

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
# set up the bot
bot = commands.Bot(
    irc_token=os.getenv('TOKEN'),
    client_id=os.getenv('CLIENT_ID'),
    nick=os.getenv('NICKNAME'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=[os.getenv('CHANNEL')]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.getenv('NICKNAME')} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.getenv('CHANNEL'), f"hello!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.getenv('NICKNAME').lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)
    if not type(ctx.content.lower()) == 'NoneType':
        if ctx.content.lower()[0] != os.getenv('BOT_PREFIX'):
            print('<'+ctx.author.name.lower()+'> '+demojize(ctx.content.lower()))


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

def botrun():
    bot.run()

if __name__ == "__main__":
    botrun()
