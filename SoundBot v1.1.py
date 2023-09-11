import os, random, asyncio, datetime, discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('VOICE_CHANNEL')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

audio_files = []
voice_client = None

ffmpeg_exe = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
default = os.path.join('Sounds', 'Default')
special = os.path.join('Sounds', 'Special', 'special.mp3')


def get_audio_files():
    audio_files.clear()
    for file in os.listdir(default):
        if file.endswith('.mp3'):
            audio_files.append(file)


@bot.event
async def on_ready():
    global voice_client, ffmpeg_exe, special, default
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}!')

    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        voice_client = await channel.connect()

    get_audio_files()

    while True:
        current_time = datetime.datetime.now()
        if (current_time.minute == 0 or current_time.minute == 30) and current_time.second == 0:
            get_audio_files()
            if voice_client.is_playing():
                voice_client.stop()
            print(f"Started at: {current_time.hour}:{current_time.minute}")
            voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_exe,
                                                     source=special))
        else:
            if not voice_client.is_playing() and audio_files:
                await asyncio.sleep(1)
                random_audio_file = random.choice(audio_files)
                print(f"Playing random audio: {random_audio_file}")
                voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_exe,
                                                         source=os.path.join(default, random_audio_file)))

        await asyncio.sleep(1)

bot.run(TOKEN)
