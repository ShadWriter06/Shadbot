import discord
import pickle
from discord.ext import commands
import time
import asyncio
import math
import random

TOKEN = 'OTkxMTM3NjAzMzc2MTMyMjEw.GD-0vp.UrGqv_N5Qrx7fVMeR2SMUYejJv85UYb8vlcA24'


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

ratingsDict = {
}

ratingsAverageDict = {

}

def findVar(parameter,string):
    x1 = 0
    y =""
    for i in string:
        if i in parameter:
            x1 = x1 + 1
        if x1 == 1:
            y += i
    return y

async def sendEmoji(emoji, message):
    emojithing = open("emoji.txt", "r")
    emojiList = emojithing.readlines()
    for i in emojiList:
        if i.startswith(":") == True:
            emojiList[emojiList.index(i)] = emojiList[emojiList.index(i)][0:len(i) - 1]
    with open('rateDictAvg.pkl', 'rb') as ratings1:
        ratingsAverageDict = pickle.load(ratings1)
    try:
        averageScore = (ratingsAverageDict[emoji])[0]
        votesCounted = (ratingsAverageDict[emoji])[1]
    except KeyError:
        averageScore = "N/A"
        votesCounted = "N/A"
    ind = emojiList.index(emoji)
    embed = discord.Embed(title=str(emoji + " sent by " + message.author.name), description=str(
        "Average Score: " + str(averageScore) + "/10 \nNumber of Votes: " + str(votesCounted)))
    embed.set_image(url=str(emojiList[ind-1]))
    embed.set_footer(text="Support Shadbot: https://www.buxland.roblux/")
    await message.channel.send(embed=embed)
    print("yes!")


@client.event
async def on_ready():
    print("ready")
    try:
        synced = await client.tree.sync()
        print("synced")
        print(synced)
    except Exception as e:
        print(e)

@client.tree.command(name="rate",description="rate an emoji using Shadbot")
async def rate(interaction: discord.Interaction,emojiname: str, rating: int):
    print(interaction.message)
    emoji = open("emoji.txt", "r")
    emojiList = emoji.readlines()
    for i in emojiList:
        if i.startswith(":") == True:
            emojiList[emojiList.index(i)] = emojiList[emojiList.index(i)][0:len(i)-1]
    emojiToRate = emojiname
    x = 0
    if emojiToRate in emojiList:
        if rating in range(0, 11):
            print("yes")
            rateKey = (str(interaction.user.id))
            print(rateKey)
            try:
                ratingList = ratingsDict[emojiToRate]
                print(ratingList)
                if rateKey in ratingList:
                    ratingList[ratingList.index(rateKey) + 1] = rating
                else:
                    ratingList.append(rateKey)
                    ratingList.append(rating)
                ratingsDict[emojiToRate] = ratingList
                with open('rateDict.pkl', 'wb') as ratings:
                    pickle.dump(ratingsDict, ratings)
                print(ratingsDict)
            except KeyError:
                ratingList = [rateKey]
                ratingList.append(rating)
                ratingsDict[emojiToRate] = ratingList
                with open('rateDict.pkl', 'wb') as ratings:
                    pickle.dump(ratingsDict, ratings)
                print(ratingsDict)
            totalScore = 0
            votesCounted = 0
            for i in ratingList:
                if int(i) < 11:
                    totalScore = totalScore + i
                    votesCounted = votesCounted + 1
            ratingsAverageDict[emojiToRate] = [round((totalScore / votesCounted), 1)]
            ratingsAverageDict[emojiToRate].append(votesCounted)
            print(ratingsAverageDict)
            with open('rateDictAvg.pkl', 'wb') as ratinger:
                pickle.dump(ratingsAverageDict, ratinger)
            await interaction.response.send_message("rated " + emojiToRate + " with a " + str(rating) + "\naverage score: " + str(
                totalScore / votesCounted) + "\n" + str(votesCounted) + " rating(s)")
        else:
            await interaction.response.send_message("rate the emoji an interger between 0 and 10")
    else:
        await interaction.response.send_message("emoji not found")



with open('rateDict.pkl', 'rb') as ratings1:
    ratingsDict = pickle.load(ratings1)

with open('rateDictAvg.pkl', 'rb') as ratingsAverage:
    ratingsAverageDict = pickle.load(ratingsAverage)

print("ratings:"+str(ratingsDict))



@client.event
async def on_message(message):
    global ratingsDict
    global ratingsAverageDict
    emoji = open("emoji.txt", "r")
    emojiList = emoji.readlines()
    for i in emojiList:
        if i.startswith(":") == True:
            emojiList[emojiList.index(i)] = emojiList[emojiList.index(i)][0:len(i)-1]
    print(emojiList)
    if message.content.startswith("shadbot addemoji") == True:
        temp = message.content[17:]
        ooo = ""
        for i in temp:
            if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890":
                ooo +=i
        temp=":"+ooo+":"
        print(temp)
        if temp not in emojiList:
            try:
                asyncio.sleep(1)
                var1 = ""
                messageID = message.id
                async for i in message.channel.history(limit=50):
                    if i.id == messageID:
                        print(str(i.attachments[0])[0:500])
                        var1 = str(i.attachments[0])[0:500]
                emojiAdd = open("emoji.txt","a")
                emojiAdd.write(var1+"\n"+temp+"\n")
                emojiAdd.close()
                await message.reply("added "+temp+" to emojis")
            except IndexError:
                await message.reply("Add an attachment you want to send, and try again")
        else:
            await message.reply("emoji already named " + temp + " in list! try again.")
    if message.content in emojiList:
        string5 = []
        for i in message.author.roles:
            string5.append(i.name)
        print(string5)
        allowedList = [755183285167980546,755178784495370340,1042277739723489331,1037500558677921894,1042277722136789002,1042278293346471996]
        if message.channel.id in allowedList:
            await sendEmoji(message.content,message)
        elif "emote bypass" in string5:
            await sendEmoji(message.content,message)
        else:
            await message.reply("send in diff channel")
    if message.content == "shadbot emojis":
        string = ""
        for i in emojiList:
            if i.startswith(":") == True:
                string = string + i + "\n"
        try:
            await message.channel.send(string)
        except discord.errors.HTTPException:
            await message.channel.send("message too long! sending as multiple messages!")
            for i in range (math.ceil(len(emojiList)/100)):
                string = ""
                for m in emojiList[(100*i):(100*i)+100]:
                    if m.startswith(":")== True:
                        string = string+m+"\n"
                await message.channel.send(string)
                asyncio.sleep(0.27)
            await message.channel.send("\n"+"Total: "+str(((len(emojiList))/2))+" emojis...")
    if message.content.startswith("shadbot rate") == True:
        zoom = message.content
        emojiToRate = ""
        rating = ""
        x = 0
        for i in zoom:
            if i == ":":
                x = x + 1
            if x == 1:
                emojiToRate = emojiToRate + i
                print(i)
        emojiToRate += ":"
        if emojiToRate in emojiList:
            final = zoom.rfind(":")
            for i in range (len(zoom)-final):
                L = zoom[i+final]
                print(str(L)+" --")
                if L.isdigit() == True:
                    rating += str(L)
            print("rating:"+rating)
            rating = int(rating)
            if rating in range(0,11):
                rateKey = (str(message.author.id))
                try:
                    ratingList = ratingsDict[emojiToRate]
                    if rateKey in ratingList:
                        ratingList[ratingList.index(rateKey)+1] = rating
                    else:
                        ratingList.append(rateKey)
                        ratingList.append(rating)
                    ratingsDict[emojiToRate] = ratingList
                    with open('rateDict.pkl', 'wb') as ratings:
                        pickle.dump(ratingsDict, ratings)
                    print(ratingsDict)
                except KeyError:
                    ratingList = [rateKey]
                    ratingList.append(rating)
                    ratingsDict[emojiToRate] = ratingList
                    with open('rateDict.pkl', 'wb') as ratings:
                        pickle.dump(ratingsDict, ratings)
                    print(ratingsDict)
                totalScore = 0
                votesCounted = 0
                for i in ratingList:
                    try:
                        if int(i) < 11:
                            totalScore = totalScore + i
                            votesCounted = votesCounted + 1
                    except ValueError:
                        print(ratingList)
                ratingsAverageDict[emojiToRate] = [round((totalScore/votesCounted),1)]
                ratingsAverageDict[emojiToRate].append(votesCounted)
                print(ratingsAverageDict)
                with open('rateDictAvg.pkl', 'wb') as ratinger:
                    pickle.dump(ratingsAverageDict, ratinger)
                print(ratingList)
                await message.reply("rated " + emojiToRate + " with a " + str(rating) + "\naverage score: "+ str(totalScore/votesCounted) + "\n" + str(votesCounted) + " rating(s)" )
            else:
                await message.reply("rate the emoji an interger between 0 and 10")
        else:
            await message.reply("emoji not found")
    if message.content == "shadbot ratings":
        placeholder = ""
        with open('rateDictAvg.pkl', 'rb') as ratingsAverage:
            ratingsAverageDict = pickle.load(ratingsAverage)
        for i in ratingsAverageDict:
            placeholder = placeholder + str(i) + " -- "+ str((ratingsAverageDict[i])[0]) + " based on "+str((ratingsAverageDict[i])[1])+ " votes\n"
        await message.reply(placeholder)
    if message.content == "sync emojis":
        emoji = open("emoji.txt", "r")
        emojiList = emoji.readlines()
        for i in emojiList:
            if i.startswith(":") == True:
                emojiList[emojiList.index(i)] = emojiList[emojiList.index(i)][0:len(i) - 1]
        print(emojiList)
        ratingsAverageDict = {}
        with open('rateDict.pkl', 'rb') as ratings1:
            ratingsDict = pickle.load(ratings1)
        for i in ratingsDict:
            print(i)
            if i in emojiList:
                ratingList = ratingsDict[i]
                totalScore = 0
                votesCounted = 0
                for q in ratingList:
                    if int(q) < 11:
                        totalScore = totalScore + q
                        votesCounted = votesCounted + 1
                ratingsAverageDict[i] = [round((int(totalScore) / int(votesCounted)),1)]
                ratingsAverageDict[i].append(votesCounted)
                print(ratingsAverageDict)
            with open('rateDictAvg.pkl', 'wb') as ratinger:
                pickle.dump(ratingsAverageDict, ratinger)
    if message.content.startswith("shadbot rating") == True:
        with open('rateDictAvg.pkl', 'rb') as ratingsAverage:
            ratingsAverageDict = pickle.load(ratingsAverage)
        if message.content == "shadbot rating top":
            emojiRankList = [":ego:"]
        elif message.content == "shadbot rating bottom":
            emojiRankList = [":redditor:"]
        print(ratingsAverageDict)
        for i in ratingsAverageDict:
            for num in range(len(emojiRankList)):
                """print(num)
                print(emojiRankList)
                print(emojiRankList[num])"""
                score1 = (ratingsAverageDict[i])[0]
                votes1 = (ratingsAverageDict[i])[1]
                score2 = (ratingsAverageDict[emojiRankList[num]][0])
                votes2 = (ratingsAverageDict[emojiRankList[num]][1])
                if message.content == "shadbot rating top":
                    if 0.25*score1*votes1+(score1-5)*votes1 > 0.25*score2*votes2+(score2-5)*votes2 :
                        emojiRankList = emojiRankList[0:num] + [i] + emojiRankList[num:]
                        break
                    else:
                        continue
                elif message.content == "shadbot rating bottom":
                    if 0.25*score1*votes1+(score1-5)*votes1 < 0.25*score2*votes2+(score2-5)*votes2 :
                        emojiRankList = emojiRankList[0:num] + [i] + emojiRankList[num:]
                        break
        placeholder1 = ""
        placeholder2 = ""
        placeholder3 = ""
        print(emojiRankList)
        for i in range(20):
            placeholder2 += str(ratingsAverageDict[emojiRankList[i]][0])+"\n"
            placeholder3 += str(ratingsAverageDict[emojiRankList[i]][1]) + "\n"
        x = 1
        for i in range(20):
            if x == 1:
                modifier = ":first_place:"
            elif x == 2:
                modifier = ":second_place:"
            elif x == 3:
                modifier = ":third_place:"
            else:
                modifier = ":heavy_minus_sign:"
            x +=1
            placeholder1 += modifier+emojiRankList[i]+"\n"
        if message.content == "shadbot rating top":
            embed = discord.Embed(title="Top Rated Emojis:",colour = discord.Colour.from_rgb(241,196,15))
        elif message.content == "shadbot rating bottom":
            embed = discord.Embed(title="Lowest Rated Emojis:",colour = discord.Colour.from_rgb(241,196,15))
        embed.add_field(name="Emoji", value=placeholder1, inline=True)
        embed.add_field(name="Rating", value=placeholder2, inline=True)
        embed.add_field(name="Votes", value=placeholder3, inline=True)
        embed.set_footer(text="Support Shadbot at this link: https://www.buxland.roblux/")
        if message.content == "shadbot rating top" or message.content == "shadbot rating bottom":
            await message.channel.send(embed=embed)
    if message.content == "shadbot random emoji":
        number1 = random.randint(0,len(emojiList)/2)*2+1
        print(number1)
        string5 = []
        for i in message.author.roles:
            string5.append(i.name)
        allowedList = [755183285167980546, 755178784495370340, 1042277739723489331, 1037500558677921894,
                       1042277722136789002, 1042278293346471996]
        if message.channel.id in allowedList:
            await sendEmoji(emojiList[number1],message)
        elif "emote bypass" in string5:
            await sendEmoji(emojiList[number1],message)
        elif message.author.id == 600755621620613121:
            await sendEmoji(emojiList[number1],message)
        else:
            await message.reply("send in diff channel")
    if message.content.startswith("shadbot details") == True:
        with open('rateDict.pkl', 'rb') as ratings1:
            ratingsDict2 = pickle.load(ratings1)
        desiredEmoji = findVar(":",message.content)+":"
        randoList = ratingsDict2[desiredEmoji]
        print(randoList)
        for thingy3 in randoList:
            if type(thingy3) == str:
                print("string"+thingy3)
                try:
                    usernam1 = await client.fetch_user(thingy3)
                    randoList[randoList.index(thingy3)] = usernam1.name
                except discord.errors.HTTPException:
                    print("error?")
        await message.reply(randoList)
    if message.content == "emojispam" and message.author.id == 627242225423613963:
        emojiSpamHappening = True
        xxx = 0
        for i in emojiList:
            if i == ":HMSledbury:":
                xxx = 1
            if emojiSpamHappening == True and xxx == 1:
                if i.startswith(":") == True:
                    await message.channel.send(i)
                    await asyncio.sleep(0.8)
    if message.content == "stopspam":
        emojiSpamHappening = False
    if message.content == "ratingsDict":
        print(ratingsDict)
    if message.content == "reset ratings":
        print(ratingsDict)
        taboolist = []
        for i in ratingsDict:
            for w in ratingsDict[i]:
                try:
                    x = int(w)
                except ValueError:
                    print(ratingsDict)
                    taboolist.append(i)
                    break
        for i in taboolist:
            ratingsDict.pop(i)
        print(ratingsDict)
        with open('rateDict.pkl', 'wb') as ratings:
            pickle.dump(ratingsDict, ratings)








client.run(TOKEN)