import discord
import time
from datetime import datetime, timedelta
import requests

client = discord.Client()  # init connection to discord

def getTime():
    now = datetime.now()  # get current datetime
    nowNice = dt_string = now.strftime("[%d/%m/%Y %H:%M:%S]")  # make it look nice for prepending
    nowEmbed = dt_string = now.strftime("%d/%m/%Y %H:%M")  # nice datetime for embed
    tomorrow = now + timedelta(hours=24)
    tomorrowEmbed = dt_string = tomorrow.strftime("%d/%m/%Y %H:%M")
    return now, nowNice, nowEmbed, tomorrow, tomorrowEmbed


@client.event
async def on_ready():  # when bot loads
    now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
    print(nowNice, 'Bot has started as {0.user}'.format(client))  # print bot username
    connectedUsers = len(client.users)
    connectedServers = len(client.guilds)
    print('Bot Online! We are serving ', connectedUsers, ' users across ', connectedServers, ' different servers!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="together (%help)"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('%status'):  # if a user types %status
        await message.channel.send(
            'Watch2gether bot is currently running and accepting commands. Please contact tomba#4032 if you are '
            'having issues.')
        await message.channel.send(
            'Serving ' + str(len(client.guilds)) + ' servers!')
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(nowNice, message.author, ' requested bot status on ', message.guild.name)  # log to console
        return

    if message.content.startswith('%about'):  # if a user types %about
        await message.channel.send(
            "Thanks for installing Watch2Gether bot! This bot is not affiliated with the Watch2Gether website.\nCheck "
            "bot status using '%status'.\nReach this page with '%about'.\nCreate a new Watch2Gether room using "
            "'%createroom'.\nBot is currently running Version 1.0.0. Please contact tomba#4032 if you have any issues "
            "with this bot.")
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(nowNice, message.author, ' requested bot about page on ', message.guild.name)  # log to console
        return

    if message.content.startswith('%help'):  # if a user types %help
        await message.channel.send(
            "Create a new room by typing '%createroom'\nCheck bot service status by typing '%status'\nRead more about "
            "the bot by typing '%about'")
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(nowNice, message.author, ' requested bot about page on ', message.guild.name)  # log to console
        return

    if message.content.startswith('%createroom'):
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(nowNice, message.author, ' requested a new room to be created. (', message.guild.name,
              ')')  # log to console
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post('https://w2g.tv/rooms/create', headers=headers)  # send request
        now, nowNice, nowEmbed, tomorrow, tomorrowEmbed = getTime()
        print(nowNice, 'Generated URL for ', message.author, 'in guild: ', message.guild.name, '(',
              response.url, ')')  # log to console
        messageAuthor = str(message.author)  # shouldn't be needed but works
        descriptionText = messageAuthor + ' has created a Watch2Gether room. Click the link to join!'
        # using + here instead of , due to strange issues
        roomURL = str(response.url)  # because why not
        embedVar = discord.Embed(title="Watch2Gether Room is Ready!", description=descriptionText,
                                 color=0x00ff00)  # create embed
        embedVar.add_field(name="Time Created", value=nowEmbed, inline=True)  # add time created field to embed
        embedVar.add_field(name="Expires", value=tomorrowEmbed, inline=True)  # add expiry field to embed
        embedVar.add_field(name="URL", value=roomURL, inline=False)  # add RoomURL to embed
        embedVar.add_field(name="Add to your server", value="https://bit.ly/2Y9npny", inline=False)  # cheeky advert
        await message.channel.send(embed=embedVar)  # send embed


client.run('xxxxx')  # run bot with this login token
