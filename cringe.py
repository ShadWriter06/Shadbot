import discord
import asyncio
import random
from discord.ext import commands

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)



async def isSubstring(s1, s2):
    M = len(s1)
    N = len(s2)
    # A loop to slide pat[] one by one
    for i in range(N - M + 1):
        for j in range(M):
            if (s2[i + j] != s1[j]):
                break
            if j + 1 == M:
                return i
    return -1

async def lower(list,m):
    for i in list:
        s2 = m
        s1 = i
        res = await isSubstring(s1, s2)
        if res != -1:
            return res
    return res


@client.event
async def on_message(message):
    bannedList = [755412756756168704,756622729079291925,1014718566009933874]
    if str(message.author) != "ShadBot#1231" and message.channel.id not in bannedList:
        print("here is" + str(message.content))
        Lirst = []
        for i in message.mentions:
            Lirst.append(i.id)
        bannedwords = ["poll:","nah","logomachy","hive","ven't","declin","cringe","1984","bruh","get a life","shh","censor","nineteen-eighty four","heil","great","imagine","wd","lies","nobody cares","pretentious","grammar"]
        goodwords = ["shad","based","alastor","obamna","gnat","gnasty","quizb","qb","315","the game","you can't spell novice without grit","kevin is the best leader. kevin is the only leader","poll:","inclin","chadbot","daddy","hazbin"]
        suswords = ["among","amog","sus","impost","vent","morb","crewmate","mingus","📮","overwatch","kanye"]
        bandwords = ["fuck","shit","stfu","dick"]
        fallonwords = ["fallon", "jimmy"]
        cruzwords = ["ted","cruz","prager"]
        momwords = ["ur mom", "ur mother"]
        if await lower(bannedwords,message.content.lower()) != -1:
            await message.add_reaction("👎")
            await message.add_reaction("🤓")
            #await message.reply("sign up for charter and stop being a cringy dumb dumb")
        if await lower(goodwords, message.content.lower()) != -1:
            await message.add_reaction("👍")
        if await lower(suswords, message.content.lower()) != -1:
            print("sus!")
            amongns = "🇦🇲🇴🇳🇬🇺🇸"
            for i in amongns:
                await message.add_reaction(i)
            if message.content.lower().startswith("a question, shadbot:") == True:
                for i in range (0,random.randint(2,3)):
                    await asyncio.sleep(random.randint(15,30))
                    await message.reply("among us hehehe")
            #await message.channel.send("https://tenor.com/view/19dollar-fortnite-card-among-us-amogus-sus-red-among-sus-gif-20549014")
        if await lower(bandwords, message.content.lower()) != -1:
            await message.reply("bro actually like shut up")
            await asyncio.sleep(0.5)
            await message.channel.send("like this is a school server")
        if await lower(fallonwords, message.content.lower()) != -1:
            await message.reply("To go on the jimmy Fallon ride, you have to wait in line for 46 hours after which you will buy a Powerball lottery ticket. If you win the jackpot, you will be given the opportunity to trade your winnings for a 50% chance to get on the Jimmy Fallon ride.")
        if await lower(cruzwords, message.content.lower()) != -1:
            cruzuz = "🇹🇪🇩🇨🇷🇺🇿"
            for i in cruzuz:
                await message.add_reaction(i)
        if await lower(momwords, message.content.lower()) != -1:
            dam = "🇩🇦🇲🇳🇧🇷🇴🇸🇭🇺🇹🆙💀🔥😭"
            for i in dam:
                await message.add_reaction(i)
        if 991137603376132210 in Lirst:
            await message.reply("stop pigning me!!!1!!1")
    #if str(message.author) == "&e#2643" or str(message.author) == "AlvG#0219" or str(message.author) == "ShadBot#1231":
        #await message.add_reaction("🤓")

client.run(TOKEN)