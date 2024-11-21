import discord # type: ignore
from discord.ext import commands # type: ignore
import yt_dlp # type: ignore
import os

# Replace with your Discord ID
OWNER_ID = 12345 #type: ignore
SONG_URL = "https://www.youtube.com/watch?v=iqS_IbuvFkQ"  # Replace with your song link



# Intents setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(name="start")
async def play(ctx):
    """Play the predefined song in the user's current voice channel."""
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None or ctx.voice_client.channel != channel:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    # Use youtube_dl to extract audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(SONG_URL, download=False)
        url = info['url']

    vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print(f"Finished playing: {e}"))
    vc.is_playing()

    await ctx.send(f"Now playing: {info['title']}")

@bot.command(name="end")
async def stop(ctx):
    """Allow only the bot owner to stop the song."""
    if ctx.author.id != OWNER_ID:
        await ctx.send("You don't have permission to stop the bot.")
        return

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped the playback.")
    else:
        await ctx.send("The bot is not playing anything.")

bot_token = os.getenv("DISCORD_BOT_TOKEN")
bot.run("Enter token here")


