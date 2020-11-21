import os
from dotenv import load_dotenv
from emoji import demojize
from twitchio.ext import commands
from twitchio import client


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
chatlog = []
# set up the bot
channels=[os.getenv('CHANNEL'), 'itsryanhiga']
bot = commands.Bot(
    irc_token=os.getenv('TOKEN'),
    client_id=os.getenv('CLIENT_ID'),
    nick=os.getenv('NICKNAME'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=channels
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
    if len(channels) == 1: chatlog.append('<'+ctx.author.name+'> '+demojize(ctx.content))
    else: chatlog.append('['+ctx.channel.name+'] <'+ctx.author.name+'> '+demojize(ctx.content))
    if len(chatlog) > 0: print(chatlog[len(chatlog)-1])
    if len(chatlog) > 0:
        with open(channels[1]+"_chat.txt", "a") as f:
            f.write(chatlog[len(chatlog)-1]+'\n')
    await bot.handle_commands(ctx)


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

async def print(ctx):
    if len(chatlog) > 0: print(chatlog[len(chatlog)-1])
    print("lmao")



def botrun():
    bot.run()

if __name__ == "__main__":
    botrun()
