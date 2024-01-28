# Initialize Background Logic
import json
from pprint import pprint
import yaml
import random as random
from secret import *
from fuzzywuzzy import fuzz
import os
import sys
import time

def string_similarity(str1, str2):
    similarity_percentage = fuzz.ratio(str1, str2)
    return similarity_percentage
def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

codeblock = '```' 

# Initialize Database
with open("data.yaml", "r") as f:
    database = yaml.safe_load(f)["Data"]
    linesdata = database['Lines']

# Initialize Discord
import discord
from discord import app_commands
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
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

    await interaction.response.send_message(f"Now starting a memory game!\nCharacter: {actor}\nScene {scene}")
    scene -= 1
    messageblock = ""
    time.sleep(1.5)
    for x in range(0, (len(linesdata[scene][f'Scene {scene+1}']))):
        
        # Check Line Matches Actor
        if actor.casefold() != (linesdata[scene][f'Scene {scene+1}'][x]['Char']).casefold():
            messageblock += (f"{linesdata[scene][f'Scene {scene+1}'][x]['Char']}: {linesdata[scene][f'Scene {scene+1}'][x]['Line']}\n") 
            print(messageblock)
            continue

        # Print Lines
        await interaction.followup.send(f"{codeblock}{messageblock}{codeblock}\n*{actor.capitalize()}, what is your line?*")

        # Wait for a user response; detect stop
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        try:
            guess = await bot.wait_for('message', timeout=240.0, check=check)
        except asyncio.TimeoutError:
            await interaction.followup.send(f"Sorry, you took too long. It was `\"{linesdata[scene][f'Scene {scene+1}'][x]['Line']}\"`\nWe will cancel your game due to inactivity.")
            break
        if (str(guess.content).casefold() is "stop"):
            break

        # Check for accuracy
        accuracy = string_similarity(str(linesdata[scene][f'Scene {scene+1}'][x]['Line']).casefold(), str(guess.content).casefold())

        if accuracy >= 80:
            await interaction.followup.send(f'You are right! You got it within {accuracy}% accuracy!')
        else:
            await interaction.followup.send(f"Oops. It is actually \"{linesdata[scene][f'Scene {scene+1}'][x]['Line']}\".")

        messageblock = ""

@bot.tree.command(name='modal')
async def modal(interaction: discord.Interaction)
    embedmessage = discord.Embed(title="Title of embed", description='description of embed', color=discord.Color.blurple)
    embedmessage.set_author("Memorization Game")

@bot.tree.command(name= 'restart')
async def restart(interaction: discord.Interaction):
    await interaction.response.send_message("Restarting bot...")
    restart_bot()

#Discord Events
@bot.event    
async def on_message(message):
    async def msg(content):
        await message.channel.send(content)
    if message.author == bot.user:
    if message.author == bot.user:
        return

    if str(message.content).casefold().startswith('say') and message.author.id == 867261583871836161:
    if str(message.content).casefold().startswith('say') and message.author.id == 867261583871836161:
        tosend = ''
        for x in range(1, (len((message.content).split())-1) + 1):
            tosend += (f' {message.content.split()[x]}')
        await msg((f'{tosend}!').strip().capitalize())



           
bot.run(secret)
