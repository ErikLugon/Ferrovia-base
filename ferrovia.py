import os
import random
import common.falas as falas
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

###Imports pro youtube
import yt_dlp as youtube_dl

##imports pro discord
import common.db_manager as db
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
status = ['TOME NO CU LEANDRO']

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
    if not daily_check.is_running():
        daily_check.start()
    # A mensagem de boas-vindas será impressa quando tudo estiver 100% pronto
    # (veja `wait_until_bot_ready_for_daily_check`).
    

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
    
# --- Contador Diário "Lores vs. Isshin" ---
COUNTER_KEY = "lores_isshin_counter"
CHANNEL_ID = 1056324441153486968
@tasks.loop(hours=1)
async def daily_check():
    # 1. Recupera o estado atual do contador
    result = db.get_global_setting(COUNTER_KEY)
    logger.debug("daily_check: raw result from db: %s", result)
    today_date = datetime.now().date()
    
    if result is None:
        # Primeira execução: inicializa o contador
        current_count = 1
        # Salva o valor inicial e a data de hoje
        logger.info("daily_check: inicializando contador para %s em %s", current_count, today_date.isoformat())
        db.set_global_setting(COUNTER_KEY, str(current_count), today_date.isoformat())
    else:
        current_count = int(result[0])
        last_update_str = result[1]
        # O db_manager armazena a data como string ISO
        last_update_date = datetime.fromisoformat(last_update_str).date()
        logger.debug("daily_check: current_count=%s last_update=%s today=%s", current_count, last_update_date, today_date)

        # 2. Verifica se um novo dia começou desde a última atualização
        if today_date > last_update_date:
            # Incrementa o contador
            new_count = current_count + 1
            # Atualiza o banco de dados com o novo valor e a data de hoje
            logger.info("daily_check: incrementando contador %s -> %s", current_count, new_count)
            db.set_global_setting(COUNTER_KEY, str(new_count), today_date.isoformat())
            # 3. Envia a mensagem no canal desejado (opcional)
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"Lores está matando o Isshin a **{new_count}** dias consecutivos.")

@daily_check.before_loop
async def wait_until_bot_ready_for_daily_check():
    # Espera até que o bot esteja pronto
    await bot.wait_until_ready()
    print("Contando quantas vezes o lores matou o Isshin...")
    
    await asyncio.sleep(0.5)
    print(f'{bot.user}: Bem vindo, Aristocrata!')

# --- Comando !isshin (Função do Bot) ---

@bot.command(name='isshin', help='Mostra o valor atual do contador de dias que Lores está matando Isshin.')
async def isshin(ctx):
    # O 'ctx' (contexto) garante que a resposta seja enviada para o canal onde o comando foi digitado.
    result = db.get_global_setting(COUNTER_KEY)
    logger.debug("command !isshin: db result=%s", result)
    if result is None:
        await ctx.send("O contador 'Lores vs. Isshin' ainda não foi inicializado. Tente novamente mais tarde.")
    else:
        current_count = int(result[0])
        # A resposta é enviada para o canal de onde veio o comando
        await ctx.send(f"Lores está matando o Isshin a **{current_count}** dias.")


# --- Comando admin !set_isshin <dias> ---
@bot.command(name='set_isshin', help='Define manualmente o contador !isshin. Uso: !set_isshin 14')
async def set_isshin(ctx, days: int):
    # Permissão restrita: apenas o dono (ID hardcoded) pode usar
    owner_id = 443844985008422934
    if ctx.author.id != owner_id:
        await ctx.send('Apenas o dono do bot pode usar este comando.')
        return
    if days < 0:
        await ctx.send('O valor do contador deve ser maior ou igual a 0.')
        return
    today_iso = datetime.now().date().isoformat()
    try:
        db.set_global_setting(COUNTER_KEY, str(days), today_iso)
        logger.info("set_isshin: %s definiu contador para %s (last_update=%s)", ctx.author, days, today_iso)
        await ctx.send(f"Contador definido para **{days}** dias. (last_update={today_iso})")
    except Exception as e:
        logger.exception("Erro ao definir contador via comando set_isshin: %s", e)
        await ctx.send('Ocorreu um erro ao definir o contador. Veja os logs.')

async def main():
    # Garantir que o banco de dados e tabelas existam antes de iniciar o bot
    db.setup_database()
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot morto à tiros pelo dono. (Erro chato de KeyboardInterrupt por conta do asyncio.run)")