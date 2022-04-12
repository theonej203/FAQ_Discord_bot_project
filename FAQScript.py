import discord
from discord.ext import commands


client = commands.Bot(command_prefix = '.')

file = open("database.txt", "w")

tokenFile = open("token.txt", "r")

@client.event
async def on_ready():
    print("bot is ready.")

    channel = discord.utils.get(client.get_all_channels(), name="moretest")

    await client.get_channel(channel.id).send("more testing")#channel id is through copy link



@client.event
async def on_message(message):
    word = message.content
    

    if message.author == client.user:
        return

    if message.content.startswith("$question"):
        word = word.split(' ', 1)[1]
        file.write(word)
        #file.close()

        await message.channel.send("answer")



    

client.run(tokenFile.read())



