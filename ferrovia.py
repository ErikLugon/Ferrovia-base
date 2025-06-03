#ferrovia.py

import os
import random
import asyncio
import falas

from dotenv import load_dotenv

import yt_dlp as youtube_dl

import discord
from discord.ext import commands
## import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
## import shutil
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
status = ['VAI TOMA NO CU LEANDRO']

'''Impede que o bot responda a si mesmo'''
async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

'''Funções'''
'''Função demostrar os status'''
@bot.event
async def on_ready():
    activity = discord.Game(name="Desista dos seus sonhos!", type=3)
    await bot.change_presence(status=discord.Status, activity=activity)
    print(f'{bot.user} se conectou!')

'''Comando de xingar uma frase aleatória'''
@bot.command(name='leandro', help='Xinga o leandro de tudo quanto é nome')
async def frases(ctx):
    response = random.choice(falas.xingamentos)
    await ctx.send(response)

'''Deez Nutz!!'''
@bot.command(name='deez', help='nutz')
async def frases(ctx):
    response = "nuts!"
    await ctx.send(response)

'''Pede pra fazer o L'''
@bot.command(name='fazueli', help='Peça para ferrovia fazer o L!')
async def frases(ctx):
    response = "L é o CARALHO rapa, eu sou robô do BOLSONARO"
    await ctx.send(response)


'''Mandar mensagem prosoto'''
@bot.command(name='send')
async def send(ctx):
    await ctx.send("Please enter the message to send:")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        message = await bot.wait_for('message', check=check, timeout=60.0)
        
        await ctx.send("Enter Id")
        def check_id(id_check):
            return id_check.author == ctx.author and id_check.channel == ctx.channel
        
        id_msg = await bot.wait_for('message', check=check_id, timeout=60.0)
        try:
            user_id = int(id_msg.content)
        except ValueError:
            await ctx.send("ID inválido. Use apenas números.")
            return

        user = bot.get_user(user_id)
        if user is None:
            await ctx.send("Usuário não encontrado no cache. Tente mencionar o usuário ou espere ele enviar uma mensagem no servidor.")
            return

        await user.send(message.content)
        await ctx.send("Mensagem enviada!")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")

'''Detecta quando alguém manda mensagem pro ferrovia e me avisa'''
@bot.event
async def on_message(message: discord.Message):
    # Check if the message is a DM and not from a bot
    if message.guild is None and not message.author.bot:
        # Log the message content and the sender
        print(f"DM from {message.author}: {message.content}")
        
        # Send message to me every time a DM is received
        user = bot.get_user(443844985008422934)
        await user.send(f"DM from {message.author} (id:{message.author.id}):\n{message.content}")
    
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

@bot.command()
async def play(ctx, url):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        voice = ctx.voice_client
        if voice.is_playing():
            voice.stop()  # Para a música atual antes de tocar a nova
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
        source = FFmpegPCMAudio(url2)
        voice.play(source)
        await ctx.send(f"Tocando: {info['title']}")
    else:
        await ctx.send("Você precisa estar em um canal de voz.")

@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Desligando o bot... 👋")
    await bot.close()

bot.run(TOKEN)
