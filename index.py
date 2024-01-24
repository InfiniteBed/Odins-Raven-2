# Initialize Background Logic
import json
from pprint import pprint
import yaml
import random as random
from secret import *



# Initialize Database
with open("data.yaml", "r") as f:
    data = yaml.safe_load(f)["Data"]
    linesdata = data['Lines']
# Initialize Discord
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#Discord Events
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('Memo Scene 2'):  
        actor = str(message).split()[3].lower()

        while True and actor != None:
            print ('Finding line that matches!')
            # Get Random Line
            number = None
            prevrng = None

            while number == prevrng:
                number = random.randint(0, (len(linesdata) - 1) )
                print(f'Random Number set to {str(number)}')
                
            # Set Values
            line = linesdata[number]['Line']
            char = linesdata[number]['Char']

            if actor == char.lower():

                # Print Lines
                await message.channel.send(char+': '+line)

            #Reset Random Number
            number = prevrng

client.run(secret)
