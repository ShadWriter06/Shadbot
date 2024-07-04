import discord
import random
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

Albums = open("albums.txt", "r", encoding="Utf8")
AlbumList = (Albums.readlines())
timeOutList = ['2023-02-24', 627242225423613963, 755136866147237961, 739951860596736011, '2023-02-25', 715271110211666070, '2023-02-26']

@client.event
async def on_message(message):
    global timeOutList
    timeOutList = timeOutList
    Songs = open("songs.txt", "r", encoding="Utf8")
    SongList = (Songs.readlines())
    lower = message.content.lower()
    if lower == "shadbot change status":
        num = random.randint(0,24)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(AlbumList[num]))
    elif lower == "o shadbot, recommend me a song":
        num = random.randint(0,len(SongList)-1)
        await message.reply(SongList[num])
        num = random.randint(0, 24)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(AlbumList[num]))
    elif lower.startswith("shadbot recommend ") == True:
        time = str(message.created_at)
        if timeOutList == [] or timeOutList[0] != time[0:10]:
            timeOutList = []
            print("timeout:" + str(timeOutList))
            print("1: "+str(timeOutList))
            timeOutList.append(time[0:10])
            print("2: "+str(timeOutList))
        if message.author.id not in timeOutList:
            timeOutList.append(message.author.id)
            print(timeOutList)
            SongWriter = open("songs.txt", "a", encoding="Utf8")
            await message.reply(message.content[18:]+ " added to list")
            SongWriter.write(message.content[18:]+ " recommended by: " + str(message.author.name) +'\n')
            SongWriter.close()
        elif message.author.id in timeOutList:
            await message.reply("Timed Out! Wait until tomorrow")



client.run(TOKEN)
