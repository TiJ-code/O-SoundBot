import os, random, asyncio, datetime, discord, requests, json
from discord.ext import commands, tasks

version = "v1.2"
GITHUB_REPO_API = "https://api.github.com/repos/TiJ-code/O-SoundBot/releases/latest"

config = json.load(open('config.json'))
paths = config['PATHS']

TOKEN = config['TOKEN']
GUILD = config['GUILD_ID']
CHANNEL_ID = config['VOICE_CHANNEL_ID']
NOTIFIER = config['NOTIFIER_ID']

ffmpeg_exe = paths['FFMPEG']
default = paths['DEFAULT']
special = paths['SPECIAL']

audio_files = []
special_file = None
voice_client = None

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)


def get_default_files():
    global audio_files, default
    audio_files.clear()
    for file in os.listdir(default):
        if file.endswith('.mp3'):
            audio_files.append(file)


def get_special_file():
    global special_file, special
    special_file = None
    local_list = []
    for file in os.listdir(special):
        if file.endswith('.mp3'):
            local_list.append(file)
    special_file = local_list[0]


@bot.event
async def on_ready():
    global voice_client, ffmpeg_exe, special, default
    global audio_files, special_file
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}!')

    check_github_release.start()

    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        voice_client = await channel.connect()

    get_default_files()
    get_special_file()

    while True:
        current_time = datetime.datetime.now()
        if (current_time.minute == 0 or current_time.minute == 30) and current_time.second == 0:

            get_default_files()
            get_special_file()

            if voice_client.is_playing() and special_file:
                voice_client.stop()

            print(f"Started at: {current_time.hour}:{current_time.minute}")
            voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_exe,
                                                     source=special))
        else:
            if not voice_client.is_playing() and audio_files:
                await asyncio.sleep(1 / 3)
                random_audio_file = random.choice(audio_files)

                print(f"Playing random audio: {random_audio_file}")
                voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_exe,
                                                         source=os.path.join(default, random_audio_file)))

        await asyncio.sleep(1)


@tasks.loop(minutes=5)
async def check_github_release():
    global NOTIFIER, GITHUB_REPO_API
    response = requests.get(GITHUB_REPO_API)    
    data = response.json()
    latest_release = data['tag_name']

    version_id = version.split('.')[1]
    latest_id = latest_release.split('.')[1]

    notified_users = NOTIFIER.split(';')

    if latest_release != version and latest_id > version_id:
        print(f'New release: {latest_release}')

        for id_ in notified_users:
            user = await bot.fetch_user(int(id_))
            await user.send(
                f'Hey {user.mention},\nthere is a **new version** of me.\n**Check out** the new version **{latest_release}** in repository TiJ_code/O-SoundBot.\n→ https://github.com/TiJ-code/O-SoundBot/releases/latest')
    elif latest_id < version_id:
        print(
            f"Heyo, i'm newer than the actual github version. Thats dope, but thats an beta version then. Maybe try to switch to a more stable version.")

        for id_ in notified_users:
            user = await bot.fetch_user(int(id_))
            await user.send(
                f"Heyo,\ni'm *newer* than the actual github version.\nThats dope, but this is probably an **beta version** here.\nMaybe try to **switch to** a more **stable version**.")


bot.run(TOKEN)
