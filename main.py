import discord
from discord.ext import commands

x = 0
y = 1

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)
messageCounter = []

"""async def testC(x,y):
  print(x+y)"""


async def MessageCounter(c, u, m, mTC):
    tM = 0
    uMD = {
    }
    r = []
    uNL = []
    async for m in c.history(limit=int(mTC)):
        tM = tM + 1
        u = str(m.author)
        if f"{m.author}" not in uMD:
            uNL.append(u)
            uMD[f"{u}"] = 1
            ###print(uMD)
        else:
            uMD[f"{u}"] = uMD[f"{u}"] + 1
            r = sorted(uNL, key=uMD.get)
    uMS = "Last " + str(mTC) + " messages:\n"
    for i in r:
        uMS = uMS + str(i) + ": " + str(uMD[f"{i}"]) + " -- " + str(
            round(100 * int(uMD[f"{i}"]) / int(tM), 2)) + "%" + "\n"
    uMS = uMS + "\n" + "Total messages counted:" + "\n" + str(tM)
    ###print(uMS)
    uMD["string"] = (uMS)
    return (uMD)


async def WordCounter(c, u, m, uMA, uMS):
    async for m in c.history(limit=1000):
        u = str(m.author)
        if f"{m.author}" not in uMA:
            uMA.append(f"{u}")
            number = 0
            for char in m.content:
                if char == " ":
                    number = number + 1
            uMA.append(number + 1)
            ###print(uMA)
        else:
            indexthing = int(uMA.index(f"{u}")) + 1
            number = 0
            for char in m.content:
                if char == " ":
                    number = number + 1
            uMA[indexthing] = int(uMA[indexthing]) + number + 1
    uMS = "Word Count: \n"
    for i in uMA:
        uMS = uMS + str(i) + "\n"
    await c.send(f"===PEOPLE WHO NEED TO SHUT UP===")
    await c.send(f"{uMS}")
    return uMA


async def combinedResults(c, mCR, wCR):
    DB = {
    }
    outputStr = ""
    for i in wCR:
        print(str(wCR))
        if type(i) != int:
            if i.startswith("string") == False:
                if i in mCR:
                    print("layer2")
                    indexNum = int(wCR.index(i)) + 1
                    words = wCR[indexNum]
                    messages = mCR[i]
                    outputStr = outputStr + str(i) + ": " + str(words) + " | " + str(
                        messages) + " | words per message: " + str(round((words / messages), 2)) + "\n"
    await c.send(f"{outputStr}")


messageCounterResult = ""
wordCounterResult = ""


@client.event
async def on_message(message):
    userMessageDict = {
    }
    messagesToCount = ""
    totalMessages = 0
    username = message.author
    userNameList = []
    userMessageArray = []
    userMessageString = ""
    channel = client.get_channel(message.channel.id)
    MessageContent = message.content
    result = []

    if message.content.startswith("shadbot last") == True:
        global messageCounterResult
        for i in message.content:
            if i.isdigit() == True:
                messagesToCount = messagesToCount + i
        messageCounterResult = await MessageCounter(channel, username, message, messagesToCount)
        await channel.send(messageCounterResult["string"])

    elif message.content.startswith("/wordsSaid") == True:
        global wordCounterResult
        wordCounterResult = await WordCounter(channel, username, message, userMessageArray, userMessageString)

    elif message.content.startswith("/combinedResults") == True:
        messageCounterResult = await MessageCounter(channel, username, message, MessageContent)
        wordCounterResult = await WordCounter(channel, username, message, userMessageArray, userMessageString)
        await combinedResults(channel, messageCounterResult, wordCounterResult)

    elif message.content.startswith("/everything") == True:
        omniscientDict = ""
        omniscientStr = ""
        text_channel_list = []
        for server in client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text':
                    text_channel_list.append(channel)
        print(text_channel_list)
        for i in text_channel_list:
            try:
                print("beninging" + str(i))
                messageCounterResult = await MessageCounter(i, username, message, 1000000)
                if omniscientDict == "":
                    omniscientDict = messageCounterResult
                    omniscientDict["string"] = 0
                else:
                    for i in messageCounterResult:
                        if i in omniscientDict:
                            if i != "string":
                                omniscientDict[i] = omniscientDict[i] + messageCounterResult[i]
                        else:
                            omniscientDict[i] = messageCounterResult[i]
                print("dictionary")
                print(omniscientDict)
            except discord.errors.Forbidden:
                print("Access Forbidden...")
        for i in omniscientDict:
            omniscientStr = omniscientStr + str(i) + ": " + str(omniscientDict[i]) + "\n"
        await message.channel.send()

        ###await channel.send(messageCounterResult["string"])


client.run(TOKEN)