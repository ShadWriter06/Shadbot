import discord
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("ready")
    try:
        synced = await bot.tree.sync()
        print("synced")
        print(synced)
    except Exception as e:
        print(e)


@bot.tree.command(name="commandone",description="test, you")
async def commandone(interaction: discord.Interaction):
    await interaction.response.send_message("hey" + thing)



print(dict)

bot.run(TOKEN)