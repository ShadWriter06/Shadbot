import pickle

import discord
import re
import datetime
from discord.ext import commands

x = 0
y = 1

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
            else:
                j = j
            if j + 1 == M:
                return i

    return -1

async def StringCounter(c, u, m, uMD, uMS, dS):
    async for m in c.history(limit=5000):
        u = str(m.author)
        content = m.content.lower()
        value = await isSubstring(dS,content)
        if value != -1:
            print("found one!")
            if u not in uMD:
                uMD[u] = 1
                print("scenario 1")
            else:
                uMD[u] = uMD[u] + 1
                print(uMD)
    uMS = dS + " Count: \n"
    for i in uMD:
        uMS = uMS + str(i) + ": " + str(uMD[i]) + "\n"
    """await c.send(f"===PEOPLE WHO NEED TO SHUT UP===")
    await c.send(f"{uMS}")"""
    return uMD

@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    username = ""
    userMessageDict = {
    }
    userMessageString = ""
    if message.content.startswith("shadbot find"):
        desiredString = ""
        x = 0
        for i in message.content:
            if i in "[]":
                x = x + 1
            if x == 1:
                desiredString += i
        desiredString = desiredString[1:]
        desiredString = desiredString.lower()
        print(desiredString)
        uMD = await StringCounter(channel,username,message,userMessageDict,userMessageString,desiredString)
        uMD = sorted(uMD.items(), key=lambda x: x[1])
        print(uMD)
        placeholder1 = ""
        placeholder2 = ""
        if len(uMD) < 15:
            for i in range(len(uMD)):
                placeholder1 += str(uMD[len(uMD) - (i + 1)][0]) + "\n"
                placeholder2 += str(uMD[len(uMD) - (i + 1)][1]) + "\n"
        else:
            for i in range(15):
                placeholder1 += str(uMD[len(uMD) - (i + 1)][0]) + "\n"
                placeholder2 += str(uMD[len(uMD) - (i + 1)][1]) + "\n"
        placeholder1 = re.sub('[()]', '', placeholder1)
        placeholder2 = re.sub('[()]', '', placeholder2)
        placeholder1 = re.sub('[,]', ':', placeholder1)
        placeholder2 = re.sub('[,]', ':', placeholder2)
        embed = discord.Embed(title="Most Uses of "+desiredString+" in last 5000 messages", colour=discord.Colour.from_rgb(255, 0, 0))
        embed.add_field(name="User", value=placeholder1, inline=True)
        embed.add_field(name="Messages", value=placeholder2, inline=True)
        embed.set_footer(text="Support Shadbot at this link: https://www.buxland.roblux/")
        await message.channel.send(embed=embed)
        print("all done!")
    elif message.content.startswith("shadbot since"):
        untilDate = message.content[14:]
        try:
            untilYear = untilDate[0:4]
            untilMonth = untilDate[5:7]
            untilDay = untilDate[8:10]
            untilEpoch = datetime.datetime(int(untilYear),int(untilMonth), int(untilDay), 0, 0).timestamp()
            print(untilEpoch)
            uMD = {

            }
            text_channel_list = []
            for server in client.guilds:
                if message.channel in server.channels:
                    for channel in server.channels:
                        if str(channel.type) == 'text':
                            text_channel_list.append(channel)
            print(text_channel_list)
            for i in text_channel_list:
                print(i)
                try:
                    async for message1 in i.history(limit=100000):
                        user1 = str(message1.author)
                        ##print(user1)
                        content = message1.content.lower()
                        messageEpoch = message1.created_at
                        messageEpoch = messageEpoch.timestamp()
                        ##print("epoch: "+str(messageEpoch))
                        if messageEpoch > untilEpoch:
                            ##print("found one!")
                            if user1 not in uMD:
                                uMD[user1] = 1
                                print("scenario 1")
                                print(uMD)
                            else:
                                uMD[user1] = uMD[user1] + 1
                                ##print(uMD)
                                ##print(message.content)
                        else:
                            break
                            print(uMD)
                            print(i)
                except discord.errors.Forbidden:
                    print("O shoot!" + str(i))
            uMS = ""
            uMD = sorted(uMD.items(), key=lambda x:x[1])
            print(uMD)
            placeholder1 = ""
            placeholder2 = ""
            if len(uMD) < 15:
                for i in range(len(uMD)):
                    placeholder1 += str(uMD[len(uMD) - (i + 1)][0]) + "\n"
                    placeholder2 += str(uMD[len(uMD) - (i + 1)][1]) + "\n"
            else:
                for i in range(15):
                    placeholder1 += str(uMD[len(uMD) - (i + 1)][0]) + "\n"
                    placeholder2 += str(uMD[len(uMD) - (i + 1)][1]) + "\n"
            placeholder1 = re.sub('[()]', '', placeholder1)
            placeholder2 = re.sub('[()]', '', placeholder2)
            placeholder1 = re.sub('[,]', ':', placeholder1)
            placeholder2 = re.sub('[,]', ':', placeholder2)
            embed = discord.Embed(title="Most Messages Since: "+untilDate, colour=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(name="User", value=placeholder1, inline=True)
            embed.add_field(name="Messages", value=placeholder2, inline=True)
            embed.set_footer(text="Support Shadbot at this link: https://www.buxland.roblux/")
            await message.channel.send(embed=embed)
            print("all done!")
        except ValueError:
            await message.reply("enter a valid date")

client.run(TOKEN)