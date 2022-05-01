import discord
from discord.ext import commands

import mysql.connector


def main():
    tokenFile = open("token.txt", "r")#file that stores the bot's token
    
    dbCursor = None


    try:#check if the database exist or not
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "root",
            database = "qnaDB"
        )

        dbCursor = db.cursor()
        

    except mysql.OperationalError as e:
        message = e.args[0]
        if message.startswith("Unknown database"):

            db = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "root"
            )

            dbCursor = db.cursor()

            dbCursor.execute("CREATE DATABASE qnaDB")#create the table questionTable and answetTable
            dbCursor.execute("CREATE TABLE questionTable (questionText VARCHAR(100), userName VARCHAR(20), courseName VARCHAR(10), id INT PRIMARY KEY AUTO_INCREMENT)")
            dbCursor.execute("CREATE TABLE answerTable (answerText VARCHAR(100), userName VARCHAR(20), questionID INT)")

        else:
            raise


    
    client = commands.Bot(command_prefix = '.')


    @client.event
    async def on_ready():
        print("bot is ready.")

        #channel = discord.utils.get(client.get_all_channels(), name="moretest")
        #await client.get_channel(channel.id).send("more testing")#channel id is through copy link



    @client.event
    async def on_message(message):
        questionID = 0
        sentMessage = message.content

        

        if(message.author == client.user):
            return



        if( message.content.startswith("$AddQuestion") ):#record the question in a database, going to use an actual database later
            dbFile = open("database.txt", "a")
            sentMessage = sentMessage.split(' ', 1)[1]
            

            #need to check the syntax for this
            dbCursor.execute("INSERT INTO questionTable (questionText, userName, courseName) VALUES (%s, %s, %s)", sentMessage, message.author.name.text, message.channel.name.text )

            await message.channel.send("Question Recorded")

        
        elif message.content.startswith("$GetAnswer"):#take in the message, scan the database for the corresponding question and send the answer to the channel
            dbFile = open("database.txt", "r")
            sentMessage = sentMessage.split(' ', 1)[1]
            getQuestion = ""

            while (True):
                
                getQuestion = dbFile.readline()
                print(sentMessage)


                if(getQuestion == ""):
                    break
                
                
                elif(sentMessage in getQuestion):
                    print("message found")
                    await message.channel.send(getQuestion)


        elif( message.content.startswith("$GetQuestion") ):
            sentMessage = sentMessage.split(' ', 1)[1]
            questionID = sentMessage.split(' ', 1)[0]#get the question id and return the question back

            dbCursor.execute("SELECT questionText FROM questionTable WHERE id =  %d", questionID)

            await message.channel.send("questionID: ",questionID, " ", dbCursor)



        
        elif( (message.author.role.name == "helper") and (message.content.startswith("$AddAnswer")) ): #make sure only authorized helper can answer question
            sentMessage = sentMessage.split(' ', 1)[1]
            questionID = sentMessage.split(' ', 1)[0]#get the question id to add the answer to the correct question

            dbCursor.execute("INSERT INTO answerTable (answerText, userName, questionId) VALUES (%s, %s, %d)", sentMessage.split(' ', 1)[1], message.author.name.text, questionID)

        

    client.run(tokenFile.read())






if (__name__ == "__main__") :
    main()
