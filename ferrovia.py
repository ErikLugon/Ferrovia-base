#ferrovia.py

import os
import random
import asyncio
import falas

from dotenv import load_dotenv

import youtube_dl

import discord
from discord.ext import commands
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import shutil
from discord.utils import get



'''Pega os arquivos do .env'''
load_dotenv()
TOKEN = os.getenv('DISCTOKEN')
GUILD = os.getenv('DISCGUILD')
print(TOKEN)


'''Pôe pra funcionar'''
intents = discord.Intents.all()
intents.members = True
intents.members = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)
status = ['Online']

'''Impede que o bot responda a si mesmo'''
async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

'''Funções'''
'''Função demostrar os status'''
@bot.event
async def on_ready():
    activity = discord.Game(name="[status template]", type=3)
    await bot.change_presence(status=discord.Status, activity=activity)
    print(f'{bot.user} se conectou!')

'''Frase aleatória'''
@bot.command(name='speak', help='[Debug] Uma frase aleatória da lista de falas')
async def frases(ctx):
    response = random.choice(falas.lines)
    await ctx.send(response)

'''Deez Nutz!!'''
@bot.command(name='deez', help='nutz')
async def frases(ctx):
    response = "deez nuts"
    await ctx.send(response)


'''Mandar mensagem'''
@bot.command(name='send')
async def send(ctx):
    await ctx.send("Please enter the message to send:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await bot.wait_for('message', check=check, timeout=60.0)
        #Manda num canal (descomenta e comenta o abaixo)
        
        # channel = bot.get_channel(766684866564849702)
        # await channel.send(message.content)
        
        #Manda pra alguém
        user = bot.get_user(593531643835318511)
        await user.send(message.content)
    except asyncio.TimeoutError:
        await ctx.send("Demorou demais pra responder!")

'''Detecta quando alguém manda mensagem pro ferrovia e me avisa'''
@bot.event
async def on_message(message: discord.Message):
    # Check if the message is a DM and not from a bot
    if message.guild is None and not message.author.bot:
        # Log the message content and the sender
        print(f"DM from {message.author}: {message.content}")
        
        # Send message to me every time a DM is received
        user = bot.get_user(443844985008422934)
        await user.send(random.choice(falas.checaOLog))
    
    # Process commands if the message is not a DM
    await bot.process_commands(message)

'''Comando de jogar cara ou coroa'''
@bot.command(name = 'coinflip', help='Joga cabeças ou caldas, tenta a sorte, pagão!')
async def caldas(ctx):
    lados = [1, 0]
    if random.choice(lados) == 1:
        embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Cabeças**! <:awesomefuckingevilblueflaimngsku:1058937734410010645>")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Caldas**! <:dododoo:1101257946383523861>" )
        await ctx.send(embed=embed)
queues = {}

'''Entra na call'''
'''Música'''
'''Entra na call'''
@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    
@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

bot.run(TOKEN)
