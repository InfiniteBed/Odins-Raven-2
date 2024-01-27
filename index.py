# Initialize Background Logic
import json
from pprint import pprint
import yaml
import random as random
from secret import *
from fuzzywuzzy import fuzz
import time

def string_similarity(str1, str2):
    similarity_percentage = fuzz.ratio(str1, str2)
    return similarity_percentage

# Initialize Database
with open("data.yaml", "r") as f:
    database = yaml.safe_load(f)["Data"]
    linesdata = database['Lines']
# Initialize Discord
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!")

@bot.tree.command(name="data")
async def data(interaction: discord.Interaction):
    await interaction.response.send_message(f"Data was sent to the logs.", ephemeral = True)
    print(f"\n\n\n\n{database}")

@bot.tree.command(name="play")
@app_commands.describe(scene = "What scene will you be memorizing?", actor = "Who are you playing?")
async def play(interaction: discord.Interaction, actor: str, scene: int):
    print("--------------------\nStarting Memory Game!")
    await interaction.response.send_message(f"Now starting a memory game!\nCharacter: {actor}\nScene {scene}")
    scene -= 1
    time.sleep(3)
    for x in range(1, 10):
        print (f"\nRound {x} of 10!")
        # Get Random Line
        number = 1
        prevrng = 1
        while actor.casefold() != (linesdata[scene][f'Scene {scene+1}'][number]['Char']).casefold():
            number = random.randint(0, (len(linesdata[scene][f'Scene {scene+1}'])) )
            print (actor.casefold())
            print ((str(linesdata[scene][f'Scene {scene+1}'][number]['Char'])).casefold())

        print('found match!!!!!!!!!!!!')
        print (actor.casefold())
        print ((linesdata[scene][f'Scene {scene+1}'][number]['Char']).casefold())
        # Print Lines
        messageblock = '```'
        for y in range(-5, 0):
            messageblock += (f"{linesdata[scene][f'Scene {scene+1}'][number+y]['Char']}: {linesdata[scene][f'Scene {scene+1}'][number+y]['Line']}\n") 
        messageblock += '```'
        await interaction.followup.send(messageblock)
        print(messageblock)

        await interaction.followup.send(f'*{actor}, what is your line?*')

        def check(m):
            return m.author == interaction.user
            
        
        try:
            guess = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await interaction.followup.send(f"Sorry, you took too long. It was `\"{linesdata[scene][f'Scene {scene+1}'][number]['Line']}\"`\nWe will cancel your game due to inactivity.")
            break
        
        if (str(guess.content).casefold() is "stop"):
            break

        accuracy = string_similarity(str(linesdata[scene][f'Scene {scene+1}'][number]['Line']).casefold(), str(guess.content).casefold())

        if accuracy >= 80:
            await interaction.followup.send(f'You are right! You got it within {accuracy}% accuracy!')
        else:
            await interaction.followup.send(f"Oops. It is actually \"{linesdata[scene][f'Scene {scene+1}'][number]['Line']}\".")

        #Reset Random Number
        number = prevrng

#Discord Eventsw
@bot.event    
async def on_message(message):
    async def msg(content):
        await message.channel.send(content)
    if message.author == bot.user:
        return

    if str(message.content).casefold().startswith('say') and message.author.id == 867261583871836161:
        tosend = ''
        for x in range(1, (len((message.content).split())-1) + 1):
            tosend += (f' {message.content.split()[x]}')
        await msg((f'{tosend}!').strip().capitalize())
           
bot.run(secret)
