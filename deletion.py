import discord
import time
from discord.ext import commands

x = 0
y = 1

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)
messageCounter = []

@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    if message.content == "/delete" and message.author.id == 627242225423613963:
        async for message in channel.history(limit=7):
            await message.delete()
            time.sleep(1)

client.run(TOKEN)