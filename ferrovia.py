import os
import random

import common.falas as falas
from data.database import create_database, seed_fishes

import asyncio
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
import logging

###Imports pro youtube
import yt_dlp as youtube_dl

##imports pro discord
import discord
from discord.ext import commands, tasks



'Pega os arquivos do .env'
load_dotenv()
TOKEN = os.getenv('DISCTOKEN')
GUILD = os.getenv('DISCGUILD')
print(TOKEN)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


'Pôe pra funcionar'
intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)
status = ['VAI TOMA NO CU LEANDRO']

'Carrega os Cogs'
initial_extensions = [
    'common.fun',
    'common.music',
    'common.fishing',
]
async def load_cogs():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"{extension} carregado.")
        except Exception as e:
            print(f"Falha ao carregar o Cog {extension}. Erro: {e}")
    

'Impede que o bot responda a si mesmo'
async def on_message(self, message):
        if message.author.id == self.user.id:
            return

'Funções'
'Função demostrar os status'

@bot.event
async def on_ready():
    activity = discord.Game(name="Desista dos seus sonhos!", type=3)
    await bot.change_presence(status=discord.Status, activity=activity)
    create_database()
    seed_fishes()
    print(f'{bot.user}: Bem vindo, Aristocrata!')
    lembrar_lores_timed.start()

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Plebeu')
    await member.add_roles(role)


'Detecta quando alguém manda mensagem pro ferrovia e me avisa'
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Oi amigo, não entendi o seu comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Ta falando grego filha da puta, me passa os argumentos direito")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem o direito de me pedir isso, plebeu")
    elif not isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Ocorreu um erro: {str(error)}")

@bot.command()
async def lembrar_lores(ctx):
    lores_id = 670333731550265402
    user = bot.get_user(lores_id)
    await user.send("Fala butzão, tudo bem? Tem o negócio com o cara lá, teu emprego e tal, esquece não fudido. Abraços, Ferrovia aqui!")
    
@tasks.loop(minutes=1)
async def lembrar_lores_timed():
    lores_id = 670333731550265402
    user = bot.get_user(lores_id)
    eu = bot.get_user(443844985008422934)
    
    if datetime.now().hour == 13 and datetime.now().minute == 00:
        await user.send("Fala butzão, tudo bem? Tem o negócio com o cara lá, teu emprego e tal, esquece não fudido. Abraços, Ferrovia aqui!")
        await eu.send("Mensagem enviada, chefe!")

@bot.check
async def roletarussa(ctx):
    if random.randint(1, 20000) == 1:
        try:
            await ctx.author.ban(reason="Memento mori né mano")
            await ctx.send(f"🎰 {ctx.author.mention} recebeu seu doce e foi de gabriel. São as atitudes né mano")
        except discord.Forbidden:
            await ctx.send(f"Ô mestre shogun, eu até ia banir o {ctx.author.mention}, mas eu não tenho permissão!!!")
        
        return False
    
    return True

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)
       

asyncio.run(main())