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
    'common.music',
]
async def load_cogs():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Cog {extension} carregado com sucesso.")
        except Exception as e:
            print(f"Falha ao carregar o Cog {extension}. Erro: {e}")
    

'Impede que o bot responda a si mesmo'
async def on_message(self, message):
        if message.author.id == self.user.id:
            return

'Funções'
'Função demostrar os status'
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='plebeu')
    await member.add_roles(role)

@bot.event
async def on_ready():
    activity = discord.Game(name="Desista dos seus sonhos!", type=3)
    await bot.change_presence(status=discord.Status, activity=activity)
    print(f'{bot.user}: Bem vindo, Aristocrata!')


'Comando de xingar uma frase aleatória'
@bot.command(name='leandro', help='Xinga o leandro de tudo quanto é nome')
async def frases(ctx):
    response = random.choice(falas.xingamentos)
    await ctx.send(response)

'Deez Nutz!!'
@bot.command(name='deez', help='nutz')
async def frases(ctx):
    response = "nuts!"
    await ctx.send(response)

'Pede pra fazer o L'
@bot.command(name='fazueli', help='Peça para ferrovia fazer o L!')
async def frases(ctx):
    response = "L é o CARALHO rapa, eu sou robô do BOLSONARO"
    await ctx.send(response)
    
@bot.command(name='poll', help='Cria uma enquete')
async def poll(ctx, *, question):
    if not question:
        await ctx.send("Por favor, forneça uma pergunta para a enquete.")
        return
    
    title = random.choice(falas.poll)
    embed = discord.Embed(title=title, description=question, color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)
    await ctx.message.delete()  # Deleta a mensagem do autor que chamou o comando
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

'Comando de jogar cara ou coroa'
@bot.command(name = 'coinflip', help='Joga cabeças ou caldas, tenta a sorte, pagão!')
async def caldas(ctx):
    lados = [1, 0]
    if random.choice(lados) == 1:
        embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Cabeças**! <:awesomefuckingevilblueflaimngsku:1058937734410010645>")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Caldas**! <:dododoo:1101257946383523861>" )
        await ctx.send(embed=embed)

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

'Mandar mensagem pra canal'
@bot.command(name='send_c', hidden=True)
@commands.has_permissions(administrator=True)
async def send_channel(ctx, channel: discord.TextChannel, *, mensagem: str):
    try:
        await channel.send(mensagem)
        await ctx.send(f"Mensagem enviada para {channel.mention}!")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para enviar mensagem nesse canal.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

'Mandar mensagem pra usuário'
@bot.command(name='send_u', hidden=True)
@commands.has_permissions(administrator=True)
async def send_user(ctx, user: discord.User, *, mensagem: str):
    try:
        await user.send(mensagem)
        await ctx.send(f"Mensagem enviada para {user}!")
    except discord.Forbidden:
        await ctx.send("Não foi possível enviar DM para esse usuário (possivelmente DMs desativadas).")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Desligando o bot... 👋")
    await bot.close()

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())