import asyncio
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
            output = (calc(message.content))
            await message.channel.send(output)  # maybe return is the problem
         except:
            await message.channel.send("fix up ur input boss")


def calc(inputStr):
    inputList = inputStr.split()
    command = inputList[0]
    if command == "$help":
        return instructions()
    elif command == "$menu":
        return menu()
    elif command == "$pick":
        return pick(inputList[1], inputList[2])
    elif command == "$choose":
        return choose(inputList[1], inputList[2])
    elif command == "$binompdf":
        return binompdf(inputList[1], inputList[2], inputList[3])
    elif command == "$binomcdf":
        return binomcdf(inputList[1], inputList[2], inputList[3])
    elif command == "$nbinompdf":
        return nbinompdf(inputList[1], inputList[2], inputList[3])
    elif command == "$dot":
        # e.g $dot 1 1 1 2 2 2 -> vectorLength is 3
        vectorLength = int((len(inputList) - 1)/2) # subtract 1 bc inputList[0] is the command
        vector1 = []
        vector2 = []
        for i in range(vectorLength):
            vector1.append(int(inputList[i+1]))
            vector2.append(int(inputList[i+1+vectorLength]))
        return dotproduct(vector1, vector2)
    elif command == "$cross":
        return crossproduct(inputList[1:4], inputList[4:])
    else:
        return "idk that formula still"


def instructions():
    return """To shout me, type the formula's name with a $ in front, followed by the numbers separated by spaces.
    e.g say '$choose 6 4' and i'll say 15
    For a list of my formulas, type $menu"""


def menu():
    return """
    $choose (n) (r) is n Choose r
    $pick (n) (r) is n Pick r
    $binompdf (n) (p) (x) is the chance of exactly x successes in n trials with a p chance of success per trial
    $binomcdf (n) (p) (x) is the chance of up to x successes in n trials with a p chance of success per trial
    $nbinomcdf (n) (p) (x) is the chance of the xth success happening on the nth trial with a p chance of success per trial"""


def pick(input1, input2):
    n = int(input1)
    r = int(input2)
    return (int(math.factorial(n) / math.factorial(n - r)))


def choose(input1, input2):
    n = int(input1)
    r = int(input2)
    return (int(math.factorial(n) / (math.factorial(r) * math.factorial(n - r))))


def binompdf(input1, input2, input3):
    trials = int(input1)
    probSuccess = float(input2)
    probFailure = 1 - probSuccess
    successes = int(input3)
    failures = trials - successes
    return ((choose(trials, successes)) * (probSuccess ** successes) * (probFailure ** failures))


def binomcdf(input1, input2, input3):
    trials = int(input1)
    probSuccess = float(input2)
    successes = int(input3)
    total = 0
    for x in range(successes + 1):
        total += binompdf(trials, probSuccess, x)
    return total


def nbinompdf(input1, input2, input3):
    trials = int(input1) - 1
    probSuccess = float(input2)
    successes = int(input3) - 1
    return choose(trials, successes) * (probSuccess ** (successes + 1)) * ((1 - probSuccess) ** (trials - successes))


def dotproduct(vectorList1, vectorList2):
    total = 0
    for i in range(len(vectorList1)):
        total += (vectorList1[i] * vectorList2[i])
    return total

def crossproduct(u, v):
    u.insert(0, 0) # for simplicity in typing up the formula
    v.insert(0, 0)

    for i in range(4): # turn inputs from str to int
        u[i] = int(u[i])
        v[i] = int(v[i])

    i = u[2]*v[3]-u[3]*v[2]
    j = -1*(u[1]*v[3]-u[3]*v[1])
    k = u[1]*v[2]-u[2]*v[1]

    return "[" + str(i) + "   " + str(j) + "   " + str(k) + "](T)"


client.run(TOKEN)
