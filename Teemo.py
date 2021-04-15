import logging

import discord

import json

with open('Champions.json', 'r', encoding="cp866") as LocalChampions:
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
Letters = Commands["letters"]


def champion_data(champ_data, champ):
    name = champ_data["name"]
    title = champ_data["title"]
    builds = LocalChampions["champions"][champ]["builds"]
    runes = LocalChampions["champions"][champ]["runes"]
    embed_var = discord.Embed(title=name + " - " + title)
    to_print = ""
    for build in builds:
        to_print += build + "\n"
    embed_var.add_field(name="Builds", value=to_print)
    to_print = ""
    for rune in runes:
        to_print += rune + "\n"
    embed_var.add_field(name="Runes", value=to_print)
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
        await message.channel.send(embed=champion_data(Champions["data"][champ], champ))

    async def champ_embed():
        embed_var = discord.Embed(title="Champions")
        champn = [number for number in range(len(ChampList))]
        alpha_counter = 0
        to_print = ""
        to_print_arr = []
        for number in champn:
            if (number%18 == 0 or number == len(ChampList)-1) and number != 0:
                embed_var.add_field(name=Letters[alpha_counter], value=to_print)
                to_print = ""
                msg = await message.channel.send(embed=embed_var)
                await champ_react(msg,number)
                embed_var = discord.Embed(title="Champions")
            if ChampList[number][0] != Letters[alpha_counter]:
                embed_var.add_field(name=Letters[alpha_counter], value=to_print)
                to_print_arr.append(to_print)
                to_print = ""
                alpha_counter += 1
            to_print += LocalChampions["champions"][ChampList[number]]["emoji"] + ":" + ChampList[number] + "\n"
        embed_var.add_field(name=Letters[alpha_counter], value=to_print)
        msg = await message.channel.send(embed=embed_var)
        await champ_react(msg, len(ChampList)-1)

    async def champ_react(msg,number):
        await msg.add_reaction('⏪')
        await msg.add_reaction('⏩')
        for number in range(number-18,number):
            try:
                await msg.add_reaction(LocalChampions["champions"][ChampList[number]]["emoji"])
            except discord.errors.Forbidden:
                print('forbidden ' + ChampList[number])
            except:
                break

    if message_content == 'champions' or message_content == 'c':
        await champ_embed()
    '''
    if message_content == 'champions' or message_content == 'c':
        embed_var = discord.Embed(title="Champions")
        to_print = ""
        alpha_counter = 0
        for number in range(19):
            if ChampList[number][0] != Letters[alpha_counter]:
                embed_var.add_field(name=Letters[alpha_counter], value=to_print)
                to_print = ""
                alpha_counter += 1
            to_print += LocalChampions["champions"][ChampList[number]]["emoji"] + ":" + ChampList[number] + "\n"
        embed_var.add_field(name=Letters[alpha_counter], value=to_print)
        msg = await message.channel.send(embed=embed_var)
        for number in range(19):
            try:
                # remove this try statement when all champ emojis are available
                await msg.add_reaction(LocalChampions["champions"][ChampList[number]]["emoji"])
            except discord.errors.Forbidden:
                print('forbidden ' + ChampList[number])
            except:
                pass
        await msg.add_reaction('⏩')
        
    if message_content == 'champions' or message_content == 'c':
        embed_var = discord.Embed(title='Champions')
        champn = [number for number in range(len(ChampList))]
        to_print = ""
        alpha_counter = 0
        for number in champn:
            if ChampList[number][0] != Letters[alpha_counter]:
                embed_var.add_field(name=Letters[alpha_counter], value=to_print)
                to_print = ""
                alpha_counter += 1
            string = LocalChampions["champions"][ChampList[number]]["emoji"] + ":" + ChampList[number] + "\n"
            to_print += string
        msg = await message.channel.send(embed=embed_var)
        for number in champn:
            try:
                # remove this try statement when all champ emojis are available
                await msg.add_reaction(LocalChampions["champions"][ChampList[number]]["emoji"])
            except discord.errors.Forbidden:
                print('forbidden ' + ChampList[number])
            except:
                pass
    '''
    if message_content == 'help' or message_content == 'h':
        embed_var = discord.Embed(title='Help')
        to_print = ""
        for command in Commands['commands']:
            to_print += command + '\n'
        embed_var.add_field(name='Commands', value=to_print)
        await message.channel.send(embed=embed_var)


if __name__ == '__main__':
    client.run('ODIyMDc0NjYwMTkwNjgzMTM2.YFM-sA.g3-RUo-YFgM55M8K9n6sm5Vnpvk')
