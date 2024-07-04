from quizbowlAPI import *
import discord
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

class MyView(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        print("yes")
        self.disabled = True
        print("!")


@bot.command() # Create a slash command
async def button(ctx):
    await ctx.reply("This is a button!", view=MyView()) # Send a message with our View class that contains the button

bot.run("OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24") # Run the bot