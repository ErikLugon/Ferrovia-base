import random
import yt_dlp as youtube_dl
import asyncio
import threading
from collections import deque, OrderedDict
import discord
from discord.ext import commands

import common.falas as falas

guild_music_states = {}

class GuildState:
    def __init__(self):
        self.queue = deque()
        self.looping = False
        self.current_song = None

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Referência ao estado global, embora seja melhor encapsular isso
        # dentro da classe Cog ou usar bot.get_cog('Musica').guild_music_states
        self.guild_music_states = guild_music_states
        # Reusar uma instância YoutubeDL para reduzir custo de inicialização
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',
        }
        try:
            self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        except Exception:
            # fallback: construa quando necessário
            self.ydl = None
        self.ydl_lock = threading.Lock()
        # Cache simples (LRU) para acelerar buscas repetidas
        self.url_cache = OrderedDict()
        self.cache_size = 128

    async def play_next_song(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states:
            self.guild_music_states[guild_id] = GuildState()
        
        state = self.guild_music_states[guild_id]

        if state.queue or state.current_song: # Verifica se há algo na fila ou tocando
            # Se looping está ativado, a música que acabou de tocar (current_song) é adicionada de volta ao final da fila
            if state.looping and state.current_song:
                state.queue.append(state.current_song)
            
            # Pega a próxima música da fila (se houver)
            if state.queue:
                next_song = state.queue.popleft()
            else:
                # Se a fila ficou vazia (e não está em loop), não há mais nada para tocar
                state.current_song = None
                return

            state.current_song = next_song
            final_audio_url = next_song['url']
            title = next_song['title']
            webpage_url = next_song['webpage_url']

            ffmpeg_options = {
                # Opções de reconexão para lidar com falhas de rede intermitentes
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                # Apenas desativa o vídeo.
                'options': '-vn' 
            }

            source = discord.FFmpegPCMAudio(final_audio_url, **ffmpeg_options)
            
            # Função de callback para tocar a próxima música.
            def after_playing(error):
                if error:
                    print(f'Erro de reprodução: {error}')
                # Agendar a corrotina no loop de eventos principal do bot de forma segura.
                # Passamos o contexto (ctx) para a próxima chamada.
                coro = self.play_next_song(ctx)
                asyncio.run_coroutine_threadsafe(coro, self.bot.loop)

            ctx.voice_client.play(source, after=after_playing)
            await ctx.send(f"Tocando agora: {title}\nLink: {webpage_url}")
        else:
            state.current_song = None
            if ctx.voice_client:
                await ctx.send("Fila de reprodução vazia. Desconectando do canal de voz.")
                await ctx.voice_client.disconnect()

    # Entra na call
    @commands.command()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("Você não está em um canal de voz!")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
        
    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            guild_id = ctx.guild.id
            if guild_id in self.guild_music_states:
                del self.guild_music_states[guild_id] # Limpa o estado da guild ao desconectar
            await ctx.send("Desconectado do canal de voz.")
        else:
            await ctx.send("Não estou em um canal de voz.")
            
    @commands.command()
    async def play(self, ctx, *, query):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states:
            self.guild_music_states[guild_id] = GuildState()
        
        state = self.guild_music_states[guild_id]

        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if not ctx.voice_client:
                await channel.connect()
            voice = ctx.voice_client

            # Check cache first
            cache_key = query.strip()
            if cache_key in self.url_cache:
                song_info = self.url_cache.pop(cache_key)
                # re-inserir para marcar como recente
                self.url_cache[cache_key] = song_info
                state.queue.append(song_info)
                await ctx.send(random.choice(falas.musica))
                if not voice.is_playing():
                    await self.play_next_song(ctx)
                else:
                    await ctx.send(f"Adicionado à fila: {song_info['title']}")
                return

            # Prepare extractor (reutiliza self.ydl quando possível)
            if not self.ydl:
                self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)

            def extract(q):
                with self.ydl_lock:
                    return self.ydl.extract_info(q, download=False)

            try:
                info = await asyncio.to_thread(extract, query)

                if 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                else:
                    entry = info

                formats = entry.get('formats') or [entry]
                audio_formats = [f for f in formats if f.get('acodec') and f.get('acodec') != 'none']
                if audio_formats:
                    best = max(audio_formats, key=lambda f: f.get('abr') or f.get('tbr') or 0)
                    final_audio_url = best.get('url')
                else:
                    final_audio_url = entry.get('url')

                title = entry.get('title')
                webpage_url = entry.get('webpage_url')

                song_info = {
                    'url': final_audio_url,
                    'title': title,
                    'webpage_url': webpage_url
                }

                # adiciona ao cache LRU
                self.url_cache[cache_key] = song_info
                if len(self.url_cache) > self.cache_size:
                    self.url_cache.popitem(last=False)

                song_info = {
                    'url': final_audio_url,
                    'title': title,
                    'webpage_url': webpage_url
                }

                state.queue.append(song_info)
                
                await ctx.send(random.choice(falas.musica))
                if not voice.is_playing():
                    await self.play_next_song(ctx)
                else:
                    await ctx.send(f"Adicionado à fila: {title}")

            except Exception as e:
                await ctx.send(f"Ocorreu um erro ao tentar tocar a música: {e}")
                print(f"Erro no comando play: {e}")
        else:
            await ctx.send("Você precisa estar em um canal de voz.")
            
    @commands.command()
    async def queue(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states or (not self.guild_music_states[guild_id].queue and not self.guild_music_states[guild_id].current_song):
            await ctx.send("A fila de reprodução está vazia.")
            return
        
        state = self.guild_music_states[guild_id]
        queue_list_str = ""
        
        if state.current_song:
            queue_list_str += f"Tocando agora: **{state.current_song['title']}**\n"
        
        if state.queue:
            queue_list_str += "\nPróximas na fila:\n"
            for i, song in enumerate(list(state.queue)):
                queue_list_str += f"{i+1}. {song['title']}\n"
        
        await ctx.send(f"Fila de reprodução:\n{queue_list_str}")
            
    @commands.command()
    async def skip(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states:
            await ctx.send("Não estou tocando nada no momento.")
            return
        
        state = self.guild_music_states[guild_id]
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Isso já chama o callback que toca a próxima música
            await ctx.send("Pulando para a próxima música...")
        elif state.queue:
            # Se não estiver tocando mas há músicas na fila, avança para a próxima
            await self.play_next_song(ctx)
            await ctx.send("Pulando para a próxima música...")
        else:
            await ctx.send("Não estou tocando nada no momento.")

    @commands.command()
    async def shuffle(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states or not self.guild_music_states[guild_id].queue:
            await ctx.send("A fila de reprodução está vazia. Não há nada para embaralhar.")
            return
        
        state = self.guild_music_states[guild_id]
        # random.shuffle não funciona diretamente com deque, converte para lista, embaralha e volta para deque
        temp_list = list(state.queue)
        random.shuffle(temp_list)
        state.queue = deque(temp_list)
        await ctx.send("Fila embaralhada!")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop() # Para a reprodução atual
            await ctx.voice_client.disconnect()
            guild_id = ctx.guild.id
            if guild_id in self.guild_music_states:
                del self.guild_music_states[guild_id] # Limpa o estado da guild ao desconectar
            await ctx.send("Parado e desconectado do canal de voz.")
        else:
            await ctx.send("Não estou em um canal de voz.")
            
    @commands.command()
    async def loop(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.guild_music_states:
            self.guild_music_states[guild_id] = GuildState()
        
        state = self.guild_music_states[guild_id]
        state.looping = not state.looping
        status = "ativado" if state.looping else "desativado"
        await ctx.send(f"Loop da fila {status}.")

async def setup(bot):
    await bot.add_cog(Music(bot))
    

