import discord
from discord.ext import commands


def main():

    tokenFile = open("token.txt", "r")#file that stores the bot's token
    dbFile = None#tempoary file to hold list of question

    numHelper = 0
    client = commands.Bot(command_prefix = '.')


    @client.event
    async def on_ready():
        print("bot is ready.")

        #channel = discord.utils.get(client.get_all_channels(), name="moretest")
        #await client.get_channel(channel.id).send("more testing")#channel id is through copy link



    @client.event
    async def on_message(message):
        questionID = 0
        word = message.content

        
        

        if(message.author == client.user):
            return


        if( message.content.startswith("$AddQuestion") ):#record the question in a database, going to use an actual database later
            dbFile = open("database.txt", "a")
            word = word.split(' ', 1)[1]
            dbFile.write(word)
            dbFile.close()

            await message.channel.send("Question Recorded")

        
        elif message.content.startswith("$GetAnswer"):#take in the message, scan the database for the corresponding question and send the answer to the channel
            dbFile = open("database.txt", "r")
            word = word.split(' ', 1)[1]
            getQuestion = ""

            while (True):
                
                getQuestion = dbFile.readline()
                print(word)


                if(getQuestion == ""):
                    break
                
                
                elif(word in getQuestion):
                    print("message found")
                    await message.channel.send(getQuestion)


        elif( message.content.startswith("$GetQuestion") ):
            word = word.split(' ', 1)[1]
            questionID = word.split(' ', 1)[0]#get the question id and return the question back

        
        elif( (message.author.role.name == "helper") and (message.content.startswith("$AddAnswer")) ): #make sure only authorized helper can answer question
            word = word.split(' ', 1)[1]
            questionID = word.split(' ', 1)[0]#get the question id to add the answer to the correct question

        

    client.run(tokenFile.read())






if (__name__ == "__main__") :
    main()
