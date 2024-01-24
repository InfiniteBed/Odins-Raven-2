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
    
    if message.content.startswith('Scene 2'):  
        actor = str(message.content).split()[2]

        for x in range(0, 10):
            print ('Finding line that matches!')
            # Get Random Line
            number = None
            prevrng = None

            while number == prevrng:
                number = random.randint(0, (len(linesdata) - 1) )
                print(f'Random Number set to {str(number)}')

            if actor.lower() == linesdata[number]['Char'].lower():

                # Print Lines
                messageblock = '```'
                for x in range(-3, 0):
                    messageblock += (f'{linesdata[number+x]['Char']}: {linesdata[number+x]['Line']}\n') 
                messageblock += '```'
                await msg(messageblock)

                await msg(f'*{actor}, what is your line?*')
                
                def check(m):
                    return m.author == message.author
                    
                
                try:
                    guess = await client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await msg(f"Sorry, you took too long. It was `\"{linesdata[number]['Line']}\"`\nWe will cancel your game due to inactivity.")
                    break

                accuracy = string_similarity(linesdata[number]['Line'], str(guess.content))

                if accuracy >= 80:
                    await message.channel.send(f'You are right! You got it within {accuracy}% accuracy!')
                else:
                    await message.channel.send(f'Oops. It is actually "{linesdata[number]['Line']}".')

                #Reset Random Number
                number = prevrng

            x+=1

        


client.run(secret)
