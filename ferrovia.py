import os
import random
import common.falas as falas
import asyncio
from dotenv import load_dotenv

###Imports pro youtube
import yt_dlp as youtube_dl

##imports pro discord
import discord
from discord.ext import commands



'Pega os arquivos do .env'
load_dotenv()
TOKEN = os.getenv('DISCTOKEN')
GUILD = os.getenv('DISCGUILD')
print(TOKEN)


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
    print(f'{bot.user}: Bem vindo, Aristocrata!')

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

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())