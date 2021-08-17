import discord
import time
from datetime import datetime, timedelta
import requests
import json
from sys import platform
import subprocess
import re
import psutil

client = discord.Client()  # init connection to discord
global cmdCount
global msgCount
global roomsCreated
cmdCount = 0
msgCount = 0
roomsCreated = 0

# API KEYS BELOW.
w2gApiKey = 'KEY'
discordApiKey = 'KEY'
botOwner = 'ID' # This should be set to your discord user ID.


def getTime():
    now = datetime.now()  # get current datetime
    nowNice = dt_string = now.strftime(
        "[%d/%m/%Y %H:%M:%S]")  # make it look nice for prepending
    nowEmbed = dt_string = now.strftime(
        "%d/%m/%Y %H:%M (GMT+0)")  # nice datetime for embed
    tomorrow = now + timedelta(hours=24)
    tomorrowEmbed = dt_string = tomorrow.strftime("%d/%m/%Y %H:%M (GMT+0)")
    return now, nowNice, nowEmbed, tomorrow, tomorrowEmbed


@client.event
async def on_ready():  # when bot loads
    now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
    print(nowNice +
          ' Bot has started as {0.user}'.format(client))  # print bot username
    connectedUsers = len(client.users)
    connectedServers = len(client.guilds)
    print("Large Servers Connected")
    for guild in client.guilds:
        if guild.large:
            print(f'{guild.name}')
    print(
        f'Bot Online! We are serving {connectedServers} different servers!'
    )  # initial 'bot ready' message. This is usually delayed, so the bot may be ready before this.
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="V2 UPDATE (%v2)"))


@client.event
async def on_message(message):
    global msgCount
    msgCount += 1
    if message.author == client.user:
        return

    if message.content.startswith('%v2'):  # if a user types %v2
        global cmdCount
        cmdCount += 1
        embedVar = discord.Embed(
            title="Watch2Gether Version 2 Changelog",
            description="Please contact tomba#4032 if you are having "
            "any issues using the new update.",
            color=0x00ff00)  # create embed
        embedVar.add_field(
            name="Major Changes",
            value=
            "You can now create a room with a starting video URL using %createroom [URL]. URL can be any video URL supported by W2G.TV\n",
            inline=False)  # createroom help
        embedVar.add_field(
            name="Minor Changes",
            value=
            "The bot now uses the official API for W2G, which should improve stability.\nW2G background color now defaults to mid grey.\nHelp and status page now use embeds as they look much better.",
            inline=True)  # status help
        embedVar.add_field(name="Add to your server",
                           value="https://bit.ly/DiscordW2G",
                           inline=False)  # cheeky advert
        await message.channel.send(embed=embedVar)
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(
            f'{nowNice} {message.author} requested bot changelog page on {message.guild.name}'
        )  # log to console
        return

    if message.content.startswith('%status'):  # if a user types %status
        cmdCount += 1
        embedVar = discord.Embed(
            title="Watch2Gether is working correctly!",
            description="Please contact tomba#4032 if you are having "
            "any issues using the bot.",
            color=0x00ff00)  # create embed
        embedVar.add_field(name="Active Servers",
                           value=str(len(client.guilds)),
                           inline=True)  # Number of active servers
        embedVar.add_field(name="Version", value="2.0.0",
                           inline=True)  # Version number
        embedVar.add_field(name="Add to your server",
                           value="https://bit.ly/DiscordW2G",
                           inline=False)  # cheeky advert
        await message.channel.send(embed=embedVar)
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(
            f'{nowNice} {message.author} requested bot status on {message.guild.name}'
        )  # log to console
        return

    if message.content.startswith('%help'):  # if a user types %help
        cmdCount += 1
        embedVar = discord.Embed(
            title="Watch2Gether Help",
            description="Please contact tomba#4032 if you are having "
            "any issues using the bot.",
            color=0x00ff00)  # create embed
        embedVar.add_field(
            name="Create a room",
            value=
            "Create a W2G room using the command %createroom [url]. (or use %cr)",
            inline=False)  # createroom help
        embedVar.add_field(
            name="Check bot status and version.",
            value="Use the command '%status to view this information.",
            inline=True)  # status help
        embedVar.add_field(name="Add to your server",
                           value="https://bit.ly/DiscordW2G",
                           inline=False)  # cheeky advert
        await message.channel.send(embed=embedVar)
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(
            f'{nowNice} {message.author} requested bot about page on {message.guild.name}'
        )  # log to console
        return

    if message.content.startswith('%createroom') or message.content.startswith(
            '%cr'):
        global roomsCreated
        cmdCount += 1
        roomsCreated += 1
        if message.content.startswith('%createroom'):
            input_url = message.content[12:]
        else:
            input_url = message.content[4:]
        validURL = False
        # Regex to check valid URL
        regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")
        p = re.compile(regex)
        if (input_url is None):
            validURL = False
        if (re.search(p, input_url)):
            validURL = True
        else:
            validURL = False
        input_url = str(
            re.sub(r'([\" \' \&])', r'\\\1',
                   input_url.replace(" ",
                                     "")))  # remove spaces and escape chars.
        if not validURL:
            await message.channel.send(
                "Please enter a valid URL. Correct format is %createroom [Video URL]"
            )
        if validURL:
            now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
            print(
                f'{nowNice} {message.author} requested a new room to be created. ({message.guild.name})'
            )  # log to console

            # Here we craft the POST data from given params.
            post_data = f'{{\"w2g_api_key\": \"{w2gApiKey}\",\"share\": \"{input_url}\",\"bg_color\": \"#4D4F51\",\"bg_opacity\": \"50\"}}'

            result = subprocess.check_output(
                f"curl --location --request POST 'https://w2g.tv/rooms/create.json' --header 'charset: utf-8' --header 'Content-Type: application/json' --data-raw '{post_data}'",
                shell=True)
            result_string = result.decode('utf-8')
            response_dict = json.loads(result_string)
            roomURL = f"https://w2g.tv/rooms/{response_dict['streamkey']}"

            now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
            print(
                f'{nowNice} Generated URL for {message.author} in guild: {message.guild.name} ({roomURL})'
            )  # log to console
            messageAuthor = str(
                message.author)  # shouldn't be needed but works
            descriptionText = f'{messageAuthor} has created a Watch2Gether room. Click the link to join!'
            embedVar = discord.Embed(title="Watch2Gether Room is Ready!",
                                     description=descriptionText,
                                     color=0x00ff00)  # create embed
            embedVar.add_field(name="Time Created",
                               value=nowEmbed,
                               inline=True)  # add time created field to embed
            embedVar.add_field(name="Expires",
                               value=tomorrowEmbed,
                               inline=True)  # add expiry field to embed
            embedVar.add_field(name="URL", value=roomURL,
                               inline=False)  # add RoomURL to embed
            embedVar.add_field(name="Add to your server",
                               value="https://bit.ly/DiscordW2G",
                               inline=False)  # cheeky advert
            await message.channel.send(embed=embedVar)  # send embed
            return

    if str(message.author.id) == f"{botOwner}":
        if message.content.startswith("%analytics"):
            print("Requested Analytics, this may take a while.")
            print(message.author.id)
            embedVar = discord.Embed(
                title="Private Stats",
                description=f"Rooms Created - {roomsCreated}",
                color=0x00ff00)  # create embed
            embedVar.add_field(name="Messages Processed Since Last Boot",
                               value=str(msgCount),
                               inline=False)
            embedVar.add_field(name="Commands Processed Since Last Boot",
                               value=str(cmdCount),
                               inline=True)
            await message.channel.send(embed=embedVar)  # send embed
            return


client.run(f'{discordApiKey}'
           )  # run bot with this login token


