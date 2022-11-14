from operator import contains
import discord
from discord import app_commands
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import asyncio
import wavelink

intents = discord.Intents.default()
intents.message_content = True

class client(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        client.loop.create_task(connect_nodes())
        print(f'Inicjalizacja sekwencji autostartu...')
        print(f'Wszystkie systemy sprawne i funkcjonalne')
        print(f'Pomyślnie zalogowano jako {client.user}')
        activity = discord.Game(name="Serving Sasha", type=3)
        await self.change_presence(status=discord.Status, activity=activity)
        await planned_message()

client = client()

tree = app_commands.CommandTree(client)
today = date.today()


async def planned_message():
    while True:
        now = datetime.now()
        then = now.replace(hour=21, minute=37, second=0)
        if then < now:
            then += timedelta(days=1)
        wait_time = (then-now).total_seconds()
        print(wait_time)
        await asyncio.sleep(wait_time-1)
        await asyncio.sleep(1)
        channel = client.get_channel(847196227984424983)
        await channel.send("Inicjalizuję sekwencję śpiewania...")
        await channel.send("Tańcz z nami tańcz dam ci pomarańczę..")

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    if "m1nt" in message.content:
        await message.add_reaction('\U0001F440')
        if "witaj m1nt" in message.content:
            await message.channel.send(f'Inicjalizuję sekwencję powitania...')
            await message.channel.send(f'Witaj {message.author}')
        if "żegnaj m1nt" in message.content:
            await message.channel.send(f'Inicjalizuję sekwencję pożegnania...')
            await message.channel.send(f'Żegnaj {message.author}')
        if "m1nt przeproś" in message.content:
            await message.channel.send(f'Inicjalizuję sekwencję przepraszania...')
            await message.channel.send(f'Beep Boop\nPrzepraszam')
        if '*pogłaszcz m1nt*' in message.content:
            await message.channel.send(f'**Mrr**'+' \U00002764')
        if 'wyświetl listę osób które pytały' in message.content:
            await message.channel.send(f'Wyświetlam listę osób, które pytały:\n``` ```')
        if ('uwu' in message.content):
            await message.channel.send(f'UwU')
        if ('owo' in message.content):
            await message.channel.send(f'OwO')
            
@tree.command(name = 'zaplanuj', description = 'Zaplanuj sesje')
async def slash(interaction: discord.Interaction, miesiac: int, dzien: int, godzina: int, minuta: int):
    t1 = datetime(year = today.year ,month = miesiac, day = dzien, hour = godzina, minute = minuta)
    f = open("terminy.txt", "w+")
    f.write(str(t1))
    f.close()
    await interaction.response.send_message(f'Zaplanowano Sesję: ' + str(t1), ephemeral = False)
   
@tree.command(name = 'przypomnij', description = 'Przypomnij frajerowi o sesji')
async def input(interaction: discord.Interaction, nazwafrajera: str):
    f = open("terminy.txt", "r+")
    t1 = f.read()
    f.close()
    await interaction.response.send_message(nazwafrajera + "\nSesja jest: " + str(t1) , ephemeral = False)

@tree.command(name = 'kiedy', description = 'Kiedy sesja')
async def input(interaction: discord.Interaction):
    f = open("terminy.txt", "r+")
    t1 = f.read()
    f.close()
    t2 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
    z1 = t2 - datetime.today()
    z1 = int(z1.total_seconds())
    z4 = int((z1/86400))
    z1 = int(z1%86400)
    z3 = int((z1/3600))
    z1 = z1%3600
    z2 = int((z1/60))
    z1 = z1%60
    await interaction.response.send_message("Sesja jest: " + str(t1) + "\nDo sesji zostało: " + str(z4) + ' Dni ' + str(z3) + ':' + str(z2) + ":" + str(z1) , ephemeral = False)


class CustomPlayer(wavelink.Player):

    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()
    loop = False
    loopsong: str



# helper function
async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host='127.0.0.1',
        port=2333,
        password='youshallnotpass',
        identifier='TEST',
        region='europe'
    )


# events

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: <{node.identifier}> is ready!')


@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if player.loop is True:
        await player.play(player.nowplaying)
    else:
        if not player.queue.is_empty:
            next_track = player.queue.get()
            player.nowplaying = next_track
            await player.play(next_track)
        else:
            await player.disconnect()

# commands

@tree.command(name = 'connect', description = 'Connect bot to your current voice channel')
async def connect(interaction: discord.Interaction):

    guild = interaction.guild
    vc = guild.voice_client

    try:
        channel = interaction.user.voice.channel
    except AttributeError:
        return await interaction.response.send_message("Please join a voice channel to connect.")

    if not vc:
        await interaction.user.voice.channel.connect(cls=CustomPlayer())
        await interaction.response.send_message("Bot connected.")
    else:
        await interaction.response.send_message("The bot is already connected to a voice channel")


@tree.command(name = 'disconnect', description = 'Disconnect bot from voice channel')
async def disconnect(interaction: discord.Interaction):
    guild = interaction.guild
    vc = guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("Bot disconnected.")
    else:
        await interaction.response.send_message("The bot is not connected to a voice channel.")
    

@tree.command(name = 'play', description = 'Play a song from url')
async def play(interaction: discord.Interaction, url: str):

    guild = interaction.guild
    vc = guild.voice_client

    track = await wavelink.YouTubeTrack.search(query=url, return_first=True)
    
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await interaction.user.voice.channel.connect(cls=custom_player)
        vc.loop = False

    if vc.is_playing():
        vc.queue.put(item=track)

        await interaction.response.send_message(embed=discord.Embed(
            title=track.title,
            url=track.uri,
            description=f"Queued: {track.title} \nChannel: {vc.channel} \nBy: {interaction.user}"
        ))
    else:
        vc.nowplaying = track
        await interaction.guild.voice_client.play(track)
        await interaction.response.send_message(embed=discord.Embed(
            title=vc.track.title,
            url=vc.track.uri,
            description=f"Playing: {vc.track.title}  \nChannel: {vc.channel} \nBy: {interaction.user}"
        ))

@tree.command(name = 'loop', description = 'Loops current song')
async def loop(interaction: discord.Interaction):
    guild = interaction.guild
    vc = guild.voice_client
    if vc.loop is False:
        vc.loop = True
        await interaction.response.send_message("Loop turned on.")
    else:
        vc.loop = False
        await interaction.response.send_message("Loop turned off.")

@tree.command(name = 'skip', description = 'Skip current song')
async def skip(interaction: discord.Interaction):
    guild = interaction.guild
    vc = guild.voice_client

    if vc:
        if not vc.is_playing():
            return await interaction.response.send_message("Nothing is playing.")
        if vc.queue.is_empty:
            await interaction.response.send_message("Skipped Song.")
            return await vc.stop()
        else:
            await interaction.response.send_message("Skipped song.") 
            await vc.seek(vc.track.length * 1000)
            if vc.is_paused():
                await vc.resume()


    else:
        await interaction.response.send_message("The bot is not connected to a voice channel.")


@tree.command(name = 'pause', description = 'Pause current playing song')
async def pause(interaction: discord.Interaction):
    guild = interaction.guild
    vc = guild.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.pause()
            await interaction.response.send_message("Paused Song.")
        else:
            await interaction.response.send_message("Nothing is playing.")
    else:
        await interaction.response.send_message("The bot is not connected to a voice channel")


@tree.command(name = 'resume', description = 'Resume current playing song')
async def resume(interaction: discord.Interaction):
    guild = interaction.guild
    vc = guild.voice_client
    if vc:
        if vc.is_paused():
            await vc.resume()
            await interaction.response.send_message("Resumed Song.")
        else:
            await interaction.response.send_message("Nothing is paused.")
    else:
        await interaction.response.send_message("The bot is not connected to a voice channel")


# error handling



client.run('MTAyMDMzODQ0NDY3NDc5NzYyOA.GJxP7P.hfjunUw5M92-RFYcp6UESjCrgOUANBZiXQey-I')