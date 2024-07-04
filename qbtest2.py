from quizbowlAPI import *
import discord
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="W👍",style=discord.ButtonStyle.success)
    async def right_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        global ppg
        global totalQuestions
        ppg += 10
        totalQuestions += 1
        await interaction.response.send_message(content="PPB: "+str(3 * ppg / totalQuestions))
        await client.change_presence(status=discord.Status.online, activity=discord.Game("PPG: " + str(3 * ppg / totalQuestions)))
        await onCorrect()

    @discord.ui.button(label="L👎", style=discord.ButtonStyle.danger)
    async def wrong_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global totalQuestions
        totalQuestions += 1
        await interaction.response.send_message(content="PPB: "+str(3 * ppg / totalQuestions))
        await client.change_presence(status=discord.Status.online, activity=discord.Game("PPG: " + str(3 * ppg / totalQuestions)))
        await onCorrect()


class NextButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Answer",style=discord.ButtonStyle.primary)
    async def right_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        global ppg
        global totalQuestions
        try:
            await interaction.response.send_message(content="PPB: "+str(3*ppg / totalQuestions))
        except ZeroDivisionError:
            await interaction.response.send_message(content="No ppb currently")
        await onNext()


def findVar(parameter,string):
    x1 = 0
    y =""
    for i in string:
        if i in parameter:
            x1 = x1 + 1
        if x1 == 1:
            y += i
    return y

def removeHTML(answer):
    answer = answer.replace("<b>", "**")
    answer = answer.replace("</b>", "**")
    answer = answer.replace("<u>", "__")
    answer = answer.replace("</u>", "__")
    answer = answer.replace("<i>", "*")
    answer = answer.replace("</i>", "*")
    return answer

global catDict
catDict = {
    "lit":"Literature",
    "sci":"Science",
    "fa":"Fine Arts",
    "rel":"Religion",
    "hist":"History",
    "myth":"Mythology",
    "ce":"Current Events",
    "ss":"Social Science",
    "philo":"Philosophy",
    "oa":"Other Academic",
    "geo":"Geography",
    "trash":"Trash"
}
subCatDict = {
    "al":"American Literature",
    "bl":"British Literature",
    "cl":"Classical Literature",
    "el":"European Literature",
    "wl":"World Literature",
    "ol":"Other Literature",
    "am":"American History",
    "anc":"Ancient History",
    "euro":"European History",
    "world":"World History",
    "oh":"Other History",
    "bio":"Biology",
    "chem":"Chemistry",
    "phys":"Physics",
    "math":"Math",
    "osci":"Other Science",
    "vfa":"Visual Fine Arts",
    "afa":"Auditory Fine Arts",
    "ofa":"Other Fine Arts",
}

global inBonus
global bonusNumber
global x
global searchtype
global qDifficulty
global qCategory
global ppg
global totalQuestions
global onAnswer
global messageChannel
inBonus = False

@client.event
async def on_message(message):
    global inBonus
    global bonusNumber
    global x
    global searchtype
    global qDifficulty
    global qCategory
    global ppg
    global totalQuestions
    global onAnswer
    global messageChannel
    if message.content == "pk categories":
        send = ""
        for i in catDict:
            send = send + i + ": " + catDict[i] + "\n"
        for i in subCatDict:
            send = send + i + ": " + subCatDict[i] + "\n"
        await message.reply(send)
    if message.content == "shadbot help me":
        await message.channel.send("Some tools at your disposal: \n -!pk (category) [difficulty]\n -pk categories (returns a list of categories)\n -clear pk")
    if inBonus == False:
        if message.content.startswith("!pk")==True:
            ppg = 0
            totalQuestions = 0
            qCategory = findVar("()",message.content)[1:]
            if qCategory in catDict:
                qCategory = catDict[qCategory]
                searchtype = "cat"
            elif qCategory in subCatDict:
                qCategory = subCatDict[qCategory]
                searchtype = "subcat"
            else:
                qCategory = ""
                searchtype = "none"
            qDifficulty = findVar("[]",message.content)[1:]
            #qSubCat = findVar("{}", message.content)[1:]
            print(qDifficulty)
            print(qCategory)
            if inBonus == False:
                inBonus = True
                bonusNumber = 0
                if searchtype == "cat":
                    x = random_question(difficulties=[int(qDifficulty)],categories=[qCategory])
                elif searchtype == "subcat":
                    x = random_question(difficulties=[int(qDifficulty)],subcategories=[qCategory])
                else:
                    inBonus == False
                if inBonus == True:
                    print(x)
                    try:
                        messageChannel = message.channel
                        embed = discord.Embed(title=str("Bonus number 1"))
                        await messageChannel.send(embed=embed)
                        embed = discord.Embed(title=str("Bonus part " + str(int(bonusNumber + 1)) + ":"),
                                              description=removeHTML(str(
                                                  x['bonuses'][0]["leadin"]+"\n"+x['bonuses'][0]["parts"][bonusNumber])))
                        await messageChannel.send(embed=embed, view=NextButton())
                    except KeyError:
                        await message.reply("use a valid category and difficulty!")
                        inBonus = False
                    except NameError:
                        await message.reply("there has been an API error. Please try again")
                        inBonus = False
                else:
                    print("use a valid category and difficulty")

@client.event
async def onNext():
    global inBonus
    global bonusNumber
    global x
    global searchtype
    global qDifficulty
    global qCategory
    global ppg
    global totalQuestions
    global onAnswer
    global messageChannel
    print("hello")
    try:
        bonusNumber += 1
        await messageChannel.send("ANSWER: " + removeHTML(x['bonuses'][0]["answers"][bonusNumber - 1]), view=Buttons())
    except IndexError:
        bonusNumber = 0
        if searchtype == "cat":
            x = random_question(difficulties=[int(qDifficulty)], categories=[qCategory])
        elif searchtype == "subcat":
            x = random_question(difficulties=[int(qDifficulty)], subcategories=[qCategory])
        await message.reply(x['bonuses'][0]["leadin"] + "\n" + x['bonuses'][0]["parts"][bonusNumber], view=NextButton())

async def onCorrect():
    global inBonus
    global bonusNumber
    global x
    global searchtype
    global qDifficulty
    global qCategory
    global ppg
    global totalQuestions
    global onAnswer
    global messageChannel
    print("hello")
    try:
        embed = discord.Embed(title=str("Bonus part "+str(bonusNumber+1) + ":"), description=removeHTML(str(x['bonuses'][0]["parts"][bonusNumber])))
        await messageChannel.send(embed=embed, view=NextButton())
    except IndexError:
        bonusNumber = 0
        embed = discord.Embed(title=str("Bonus number " + str(int((totalQuestions/3)+1))))
        await messageChannel.send(embed=embed)
        if searchtype == "cat":
            x = random_question(difficulties=[int(qDifficulty)], categories=[qCategory])
            embed = discord.Embed(title=str("Bonus part " + str(int(bonusNumber+1)) + ":"),
                                  description=removeHTML(str(x['bonuses'][0]["leadin"] + "\n" + x['bonuses'][0]["parts"][bonusNumber])))
            await messageChannel.send(embed=embed, view=NextButton())
        elif searchtype == "subcat":
            x = random_question(difficulties=[int(qDifficulty)], subcategories=[qCategory])
            embed = discord.Embed(title=str("Bonus part " + str(int(bonusNumber+1)) + ":"),
                                  description=removeHTML(str(x['bonuses'][0]["leadin"] + "\n" + x['bonuses'][0]["parts"][bonusNumber])))
            await messageChannel.send(embed=embed, view=NextButton())

client.run(TOKEN)