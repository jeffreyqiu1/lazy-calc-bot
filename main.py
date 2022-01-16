import math

import discord
import os

client = discord.Client()

TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        try:
            await message.channel.send(calc(message.content)) # turn into str?
        except:
            await message.channel.send("incorrect input")

def calc(inputStr):
    inputList = inputStr.split()
    command = inputList[0]

    commandDictionary = {
        "$pick": pick(inputList[1], inputList[2]),
        "$choose": choose(inputList[1], inputList[2]),
        #"$binompdf": binompdf(inputList[1], inputList[2], inputList[3])
    }
    return commandDictionary.get(command, "command not found")

def pick(input1, input2):
    n = int(input1)
    r = int(input2)
    return (int(math.factorial(n)/math.factorial(n-r)))

def choose(input1, input2):
    n = int(input1)
    r = int(input2)
    return (int(math.factorial(n)/(math.factorial(r)*math.factorial(n-r))))

def binompdf(input1, input2, input3):
    trials = int(input1)
    probSuccess = float(input2)
    probFailure = 1 - probSuccess
    successes = int(input3)
    failures = trials - successes
    return ((choose(trials, successes))*(probSuccess**successes)*(probFailure**failures))

client.run(TOKEN)