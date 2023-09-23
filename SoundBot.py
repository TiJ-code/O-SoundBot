import os, random, asyncio, datetime, discord, requests
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()

version = "v1.2"
GITHUB_REPO_API = "https://api.github.com/repos/TiJ-code/O-SoundBot/releases/latest"

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('VOICE_CHANNEL')
GUILD = os.getenv('GUILD_ID')
NOTIFIER = os.getenv('NOTIFIER')

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

    check_github_release.start()

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


newVersionReminder = False
newVersionCounter = 0

@tasks.loop(minutes=5)
async def check_github_release():
    global NOTIFIER, GITHUB_REPO_API, newVersionReminder, newVersionCounter
    response = requests.get(GITHUB_REPO_API)
    data = response.json()
    latest_release = data['tag_name']

    version_id = version.split('.')[1]
    latest_id = latest_release.split('.')[1]

    if newVersionCounter >= 12:
        newVersionCounter = 0
        newVersionReminder = False

    if latest_release != version and latest_id > version_id and not newVersionReminder:
        print(f'New release: {latest_release}')
        newVersionReminder = True
        newVersionCounter += 1
        user = await bot.fetch_user(int(NOTIFIER))
        await user.send(f'Hey {user.mention},\nthere is a **new version** of me.\n**Check out** the new version **{latest_release}** in repository TiJ_code/O-SoundBot.\n→ https://github.com/TiJ-code/O-SoundBot/releases/tag/latest')
    elif latest_id < version_id:
        print(f"Heyo, i'm newer than the actual github version. Thats dope, but thats an beta version then. Maybe try to switch to a more stable version.")

        user = await bot.fetch_user(int(NOTIFIER))
        await user.send(f"Heyo,\ni'm *newer* than the actual github version.\nThats dope, but this is probably an **beta version** here.\nMaybe try to **switch to** a more **stable version**.")

bot.run(TOKEN)
