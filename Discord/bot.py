import os, asyncio, random, discord, youtube_dl, signal
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN'); GUILD = os.getenv('DISCORD_GUILD_ID')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

description = '''A L I C E.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='cum', description=description, intents=intents)

class storage:
    def __init__(self, songlist, ctx):
        self.songlist = songlist
        self.ctx = ctx

g = storage(None, None)
songs = asyncio.Queue()
play_next_song = asyncio.Event()

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

@bot.command()
async def play(ctx, *, query):
    """Plays a file from the local filesystem"""

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(query))

@bot.command()
async def yt(ctx, *, url):
    """Plays from a url (almost anything youtube_dl supports)"""

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))

@bot.command()
async def queue(ctx, *, url):
    """Plays from a queue (almost anything youtube_dl supports)"""
    if g.songlist == None: g.songlist={i.id:[] for i in bot.guilds}
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)

        g.songlist[ctx.message.guild.id].append(player)
        g.ctx=ctx
        loop = asyncio.get_event_loop()
        #if not movequeue_true and bot.loop.is_running():
        # await movequeue()
        asyncio.ensure_future(movequeue())

    await ctx.send('Queued: {}'.format(player.title))

async def movequeue():
    while True:
        if g.ctx == None:
            return "bitchass"
        print('moove')
        if not g.ctx.voice_client.is_playing():
            if len(g.songlist[g.ctx.message.guild.id])!=0:
                player = g.songlist[g.ctx.message.guild.id].pop(0)
                return g.ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            return 'queue is empty'

@bot.command()
async def stream(ctx, *, url):
    """Streams from a url (same as yt, but doesn't predownload)"""

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))

@bot.command()
async def volume(ctx, volume: int):
    """Changes the player's volume"""

    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel.")

    ctx.voice_client.source.volume = volume / 100
    await ctx.send("Changed volume to {}%".format(volume))

@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()

@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()

@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await movequeue()

@bot.command()
async def leave(ctx):
    """Stops and disconnects the bot from voice"""
    if g.songlist != None and g.ctx.message.guild.id in g.songlist:
        g.songlist[g.ctx.message.guild.id] = []
    await g.ctx.voice_client.disconnect()

@play.before_invoke
@yt.before_invoke
@stream.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

@queue.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for guild in bot.guilds:
        print('\n\n'+
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
    game = discord.Game("CUM")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.listen('on_message')
async def CUM(message):
    await movequeue()
    channel = bot.get_channel(message.channel.id)
    if message.author.id!=bot.user.id and str(message.guild.id) == str(GUILD) and str(channel)=='ping':
        await channel.send('CUM')
        for i in [283321502143741972, 392577192359624706, 337329313860812800]:
            user = bot.get_user(i)
            await user.send(message.content)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
loop = asyncio.get_event_loop()
print(loop)
# try:
#     loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
#     loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())
# except NotImplementedError:
#     pass
bot.run(TOKEN)
