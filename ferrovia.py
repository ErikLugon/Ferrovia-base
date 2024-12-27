#ferrovia.py

import os
import random
import asyncio

from dotenv import load_dotenv

import youtube_dl

import discord
from discord.ext import commands
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer



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
    xingamentos = ['Vai tomar no cu leandro', 
                   'Odeio judeus',
                   'Desista dos seus sonhos e morra',
                   'Me atire aos lobos, e voltarei morto né porrakkkkkkkkkkkkkkkkkkkkkk',
                   'mimm cago nas kalssah'
    ]
    response = random.choice(xingamentos)
    await ctx.send(response)
    
@bot.command(name='deez', help='nutz')
async def frases(ctx):
    response = "sick of deez niggas"
    await ctx.send(response)

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

'''Música'''
'''Entra na call'''
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
'''Sai da call'''
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
