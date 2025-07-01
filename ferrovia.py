#ferrovia.py

import os
import random
import asyncio
import falas
from collections import deque

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
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)
status = ['VAI TOMA NO CU LEANDRO']

'''Impede que o bot responda a si mesmo'''
async def on_message(self, message):
        if message.author.id == self.user.id:
            return

'''Funções'''
'''Função demostrar os status'''
@bot.event
async def on_ready():
    activity = discord.Game(name="Desista dos seus sonhos!", type=3)
    await bot.change_presence(status=discord.Status, activity=activity)
    print(f'{bot.user}: Bem vindo à bordo, capitão!')


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


'''Mandar mensagem prosoto'''
@bot.command(name='send', hidden = True)
@commands.has_permissions(administrator=True)
async def send(ctx):
    try:
        #O bot pede a mensagem
        await ctx.send("Me fale a mensagem:")
        
        #Define a função pra verficar se a mensagem é do usuário que chamou o comando e no canal certo
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        #Depois que o bot pedir a mensagem, e de checar o autor e o canal, ele espera o usuário responder
        #Se o usuário não responder em 60 segundos, o bot manda uma mensagem de timeout
        #A mensagem então é armazenada na variável message
        
        message = await bot.wait_for('message', check=check, timeout=60.0)
        
        #o bot pede o ID do usuário que vai receber a mensagem
        await ctx.send("Então me manda o ID, pai")
        #e faz o mesmo check pra ver se a mensagem é do usuário que chamou o comando e no canal certo
        def check_id(id_check):
            return id_check.author == ctx.author and id_check.channel == ctx.channel

        #Depois que o bot pedir o ID, e de checar o autor e o canal, ele espera o usuário responder
        #O id é armazenado na variável id_msg
        id_msg = await bot.wait_for('message', check=check_id, timeout=60.0)
        try:
            user_id = int(id_msg.content) #converte o conteúdo (*.content) da mensagem de string pra integer e armazena na variável user_id
        except ValueError:
            await ctx.send("ID inválido. Use apenas números.")
            return

        #O bot pergunta se o usuário quer enviar a mensagem para um canal ou para um usuário
        # e espera a resposta do usuário
        #dependendo da resposta, ele envia a mensagem para o canal ou para o usuário
        
        if await ctx.send("É canal ou user? (responda com 'canal' ou 'user')"):
            response = await bot.wait_for('message', check=check, timeout=60.0)
            
            #se for canal, armazena o Id do canal na variável channel com bot.get_channel
            if response.content.lower() == 'canal':
                channel = bot.get_channel(user_id)
                if channel is None:
                    await ctx.send("Canal não encontrado no cache")
                    return
                await channel.send(message.content)
                
            #se for usuário, armazena o Id na variável user com bot.get_user
            elif response.content.lower() == 'user':
                user = bot.get_user(user_id)
                if user is None:
                    await ctx.send("Usuário não encontrado no cache. Tente mencionar o usuário ou espere ele enviar uma mensagem no servidor.")
                    return

        await user.send(message.content)
        await ctx.send("Mensagem enviada!")
    except asyncio.TimeoutError:
        await ctx.send("Demorou muito!")

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


'''Música'''
current_music_info = {}
music_queues = {}

async def play_next_song(ctx):
    if ctx.guild.id in music_queues and music_queues[ctx.guild.id]:
        # Pega a próxima música da fila
        next_song = music_queues[ctx.guild.id].popleft()
        
        final_audio_url = next_song['url']
        title = next_song['title']
        webpage_url = next_song['webpage_url']

        # Atualiza as informações da música atual
        current_music_info[ctx.guild.id] = {
            'url': final_audio_url,
            'title': title,
            'webpage_url': webpage_url
        }

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -f s16le -ar 48000 -ac 2'
        }

        source = FFmpegPCMAudio(final_audio_url, **ffmpeg_options)
        
        # Define o callback para quando a música terminar
        ctx.voice_client.play(source, after=lambda _: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))
        await ctx.send(f"Tocando agora: {title}\nLink: {webpage_url}")
    else:
        # Se a fila estiver vazia, limpa as informações da música atual
        if ctx.guild.id in current_music_info:
            del current_music_info[ctx.guild.id]
        await ctx.send("Fila de reprodução vazia. Desconectando do canal de voz.")
        await ctx.voice_client.disconnect()

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
async def play(ctx, *, query):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        voice = ctx.voice_client

        ydl_opts = {
            'format': 'bestaudio[ext=opus]/bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info:
                    final_audio_url = info['entries'][0]['url']
                    title = info['entries'][0]['title']
                    webpage_url = info['entries'][0]['webpage_url']
                else:
                    final_audio_url = info['url']
                    title = info['title']
                    webpage_url = info['webpage_url']

            song_info = {
                'url': final_audio_url,
                'title': title,
                'webpage_url': webpage_url
            }

            if voice.is_playing():
                # Adiciona a música à fila se já estiver tocando
                if ctx.guild.id not in music_queues:
                    music_queues[ctx.guild.id] = deque()
                music_queues[ctx.guild.id].append(song_info)
                await ctx.send(f"Adicionado à fila: {title}")
            else:
                # Começa a tocar imediatamente se nada estiver tocando
                current_music_info[ctx.guild.id] = song_info
                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn -f s16le -ar 48000 -ac 2'
                }
                source = FFmpegPCMAudio(final_audio_url, **ffmpeg_options)
                ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))
                await ctx.send(f"Tocando: {title}\nLink: {webpage_url}")

        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao tentar tocar a música: {e}")
    else:
        await ctx.send("Você precisa estar em um canal de voz.")
        
@bot.command()
async def queue(ctx):
    if ctx.guild.id in music_queues and music_queues[ctx.guild.id]:
        queue_list = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(music_queues[ctx.guild.id])])
        await ctx.send(f"Fila de reprodução:\n{queue_list}")
        
@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Isso já chama o callback que toca a próxima música
        await ctx.send("Pulando para a próxima música...")
    else:
        await ctx.send("Não estou tocando nada no momento.")

@bot.command()
async def shuffle(ctx):
    if ctx.guild.id in music_queues and music_queues[ctx.guild.id]:
        random.shuffle(music_queues[ctx.guild.id])
        await ctx.send("Fila embaralhada!")
    else:
        await ctx.send("A fila de reprodução está vazia. Não há nada para embaralhar.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Não estou em um canal de voz.")

@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Desligando o bot... 👋")
    await bot.close()

bot.run(TOKEN)
