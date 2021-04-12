import logging

import discord

import json

with open('Champions.json','r',encoding="cp866") as LocalChampions:
    LocalChampions = json.load(LocalChampions)
with open('champion.json', 'r', encoding="cp866") as Champions:
    Champions = json.load(Champions)
with open('commands.json', 'r', encoding='cp866') as Commands:
    Commands = json.load(Commands)
ChampList = []
LowerChampList = []
for Champion in Champions["data"]:
    ChampList.append(Champion)
    LowerChampList.append(Champion.lower())
Letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def champion_data(champ_data,champ):
    name = champ_data["name"]
    title = champ_data["title"]
    builds = LocalChampions["champions"][champ]["builds"]
    runes = LocalChampions["champions"][champ]["runes"]
    embed_var = discord.Embed(title=name + " - " + title)
    toPrint = ""
    for build in builds:
        toPrint += build + "\n"
    embed_var.add_field(name="Builds", value=toPrint)
    toPrint = ""
    for rune in runes:
        toPrint += rune + "\n"
    embed_var.add_field(name="Runes", value=toPrint)
    return embed_var


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_ready():
    activity = discord.Game(name="|help", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or message.content[0] != "|":
        return

    message_content = message.content.lower()
    message_content = message_content[1:]

    if message_content == "wukong":
        message_content = "monkeyking"

    if message_content in LowerChampList:
        champ = LowerChampList.index(message_content)
        champ = ChampList[champ]
        await message.channel.send(embed=champion_data(Champions["data"][champ],champ))

    if message_content == 'champions' or message_content == 'c':
        embed_var = discord.Embed(title='Champions')
        champn = [number for number in range(len(ChampList))]
        toPrint = ""
        alphaCounter = 0
        for number in champn:
            if ChampList[number][0] != Letters[alphaCounter]:
                embed_var.add_field(name=Letters[alphaCounter], value=toPrint)
                toPrint = ""
                alphaCounter += 1
            string = LocalChampions["champions"][ChampList[number]]["emoji"] + ":" + ChampList[number] +"\n"
            toPrint += string
        msg = await message.channel.send(embed=embed_var)
        for number in champn:
            try:
                #remove this try statement when all champ emojis are available
                await msg.add_reaction(LocalChampions["champions"][ChampList[number]]["emoji"])
            except discord.errors.Forbidden:
                print('forbidden '+ChampList[number])
            except:
                pass

    if message_content == 'help' or message_content == 'h':
        embed_var = discord.Embed(title='Help')
        toPrint = ""
        for command in Commands['commands']:
            toPrint += command + '\n'
        embed_var.add_field(name='Commands',value=toPrint)
        await message.channel.send(embed=embed_var)


client.run('TOKEN HERE')
