import os, random, asyncio, datetime, requests, discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('VOICE_CHANNEL')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(intents=intents)

audio_files = []
voice_client = None

notifier_user_id_str = os.getenv('NOTIFIER')
if notifier_user_id_str:
    notifier_user_id = notifier_user_id_str.split(',')
else:
    notifier_user_id = []
notifier_user_id = [int(user_id) for user_id in notifier_user_id]    # Convert user IDs to ints

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
    global voice_client, notifier_user_id, ffmpeg_exe, special, default
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}!')

    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        voice_client = await channel.connect()

    get_audio_files()
    guild = bot.get_guild(int(os.getenv('GUILD')))
    users = []

    if guild:
        for notifier in notifier_user_id:
            users.append(guild.get_member(int(notifier)))

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
