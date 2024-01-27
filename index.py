# Initialize Background Logic
import json
from pprint import pprint
import yaml
import random as random
from secret import *
from fuzzywuzzy import fuzz

def string_similarity(str1, str2):
    similarity_percentage = fuzz.ratio(str1, str2)
    return similarity_percentage

# Initialize Database
with open("data.yaml", "r") as f:
    data = yaml.safe_load(f)["Data"]
    linesdata = data['Lines']
# Initialize Discord
import discord
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#Discord Events
@client.event    
async def on_message(message):
    async def msg(content):
        await message.channel.send(content)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await msg('Hello!')

    if str(message.content).lower().startswith('say') and message.author.id == 867261583871836161:
        tosend = ''
        for x in range(1, (len((message.content).split())-1) + 1):
            tosend += (f' {message.content.split()[x]}')
        await msg((f'{tosend}!').strip().capitalize())
    
    if message.content.startswith('Scene 2'):  
        actor = str(message.content).split()[2]
        print(f"--------------------\nStarting Memory Game!")
        for x in range(0, 10):
            print (f"\nRound {x} of 10!")
            # Get Random Line
            number = 1
            prevrng = 1
            while number == prevrng and actor.lower() != str(linesdata[number]['Char']).lower():
                number = random.randint(0, (len(linesdata) - 1) )

            print('found match')

            # Print Lines
            messageblock = '```'
            for y in range(-3, 0):
                messageblock += (f"{linesdata[number+y]['Char'  ]}: {linesdata[number+y]['Line']}\n") 
            messageblock += '```'
            await msg(messageblock)
            print(messageblock)

            await msg(f'*{actor}, what is your line?*')
            
            def check(m):
                return m.author == message.author
                
            
            try:
                guess = await client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await msg(f"Sorry, you took too long. It was `\"{linesdata[number]['Line']}\"`\nWe will cancel your game due to inactivity.")
                break

            accuracy = string_similarity(str(linesdata[number]['Line']).lower(), str(guess.content).lower())

            if accuracy >= 80:
                await message.channel.send(f'You are right! You got it within {accuracy}% accuracy!')
            else:
                await message.channel.send(f"Oops. It is actually \"{linesdata[number]['Line']}\".")

            #Reset Random Number
            number = prevrng

        


client.run(secret)
