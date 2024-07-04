import discord
import PIL
from PIL import Image
import random
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True


image = Image.open('doggie.png')

client = commands.Bot(command_prefix='/', intents=intents)

msgDict = {}


@client.event
async def on_message(message):
    global msgDict
    print(message.content)
    lower = message.content.lower()
    """if str(message.author) == "AlvG#0219":
        await message.reply("omg change ur profile pic cringe cringe cringe")
    elif str(message.author) == "ShadBot#1231" and message.content == "omg change ur profile pic cringe cringe cringe":
        await message.reply("no cringe")"""
    if lower == "ratio":
        if str(message.author) == "Hex#8583" or str(message.author) == "AlvG#0219" or str(message.author) == "ShadBot#1231" or str(message.author) == "&e#2643":
            await message.add_reaction("👍")

        else:
            await message.add_reaction("👍")
            await message.add_reaction("👎")
    elif lower == "spelling" or lower == "speiing":
        await message.reply("ratio")
    elif lower == "315":
        await message.add_reaction("🧠")
    elif lower == "shadbot tell me a joke":
        await message.reply("you.")
    elif lower == "🤨":
        await message.channel.send("https://tenor.com/view/rock-one-eyebrow-raised-rock-staring-the-rock-gif-22113367")
    elif lower == "shadbot help me":
        commandString = "Tools at your disposal: \n \n"
        commands = open("commands.txt","r")
        commandList = commands.readlines()
        for i in commandList:
            commandString = commandString + i
        await message.channel.send(commandString)
    elif lower == ":doggie:":
        await message.channel.send(file=discord.File(r'doggie.png'))
    elif lower == "hi shad":
        await message.reply("hello there")
    elif lower.startswith("a question, shadbot:") == True:
        x = random.randint(0,12)
        w = random.randint(0,9)
        shlist = ["yes","yes","no","no","maybe","idk man","yeah!","nope, and never","not a bit","ong","fr","kinda","no, not really"]
        await message.reply(shlist[x])
        if w == 9:
            await message.channel.send("it's bushin time")
    try:
        if lower in msgDict:
            msgDict[lower] += 1
            print(msgDict)
            if msgDict[lower] >= 3 and message.author.id != 991137603376132210:
                await message.channel.send("stop spamming bozo")
        else:
            msgDict = {}
            msgDict[lower] = 1
            print(msgDict)
    except:
        print("whoops")
    if lower == "shadbot most edited messages":
        msgDict2 = {}
        async for i in message.channel.history(limit=5000):
            if i.edited_at != None:
                if i.author.name in msgDict2:
                    msgDict2[i.author.name] += 1
                else:
                    msgDict2[i.author.name] = 1
        await message.reply("most edited messages in the last 5000 messages:\n"+str(msgDict2))
    if lower.startswith("imagine") == True:
        await message.channel.send("ong")
    if lower.endswith("-") == True:
        await message.add_reaction("👎")
        await message.add_reaction("🤓")
    if lower == "rip shad" and message.author.id == 627242225423613963:
        await message.channel.send("goodbye")
        await message.channel.send("imma take an extended break")



client.run(TOKEN)