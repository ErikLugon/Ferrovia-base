import random
import discord
from discord.ext import commands

import common.falas as falas


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='leandro', help='Xinga o leandro de tudo quanto é nome')
    async def leandro(self, ctx):
        """Comando de xingar uma frase aleatória"""
        response = random.choice(falas.xingamentos)
        await ctx.send(response)

    @commands.command(name='deez', help='nutz')
    async def deez(self, ctx):
        """Deez Nutz!!"""
        response = "nuts!"
        await ctx.send(response)

    @commands.command(name='fazueli', help='Peça para ferrovia fazer o L!')
    async def fazueli(self, ctx):
        """Pede pra fazer o L"""
        response = "L é o CARALHO rapa, eu sou robô do BOLSONARO"
        await ctx.send(response)
        
    @commands.command(name='poll', help='Cria uma enquete')
    async def poll(self, ctx, *, question):
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
    @commands.command(name = 'coinflip', help='Joga cabeças ou caldas, tenta a sorte, pagão!')
    async def caldas(self, ctx):
        lados = [1, 0]
        if random.choice(lados) == 1:
            embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Cabeças**! <:awesomefuckingevilblueflaimngsku:1058937734410010645>")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Cabeças ou caldas!!!", description=f"{ctx.author.mention} Girou a moeda, e ela concedeu **Caldas**! <:dododoo:1101257946383523861>" )
            await ctx.send(embed=embed)
        
    'Mandar mensagem pra canal'
    @commands.command(name='send_c', hidden=True)
    @commands.has_permissions(administrator=True)
    async def send_channel(self, ctx, channel: discord.TextChannel, *, mensagem: str):
        try:
            await channel.send(mensagem)
            await ctx.send(f"Mensagem enviada para {channel.mention}!")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para enviar mensagem nesse canal.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")

    'Mandar mensagem pra usuário'
    @commands.command(name='send_u', hidden=True)
    @commands.has_permissions(administrator=True)
    async def send_user(self, ctx, user: discord.User, *, mensagem: str):
        try:
            await user.send(mensagem)
            await ctx.send(f"Mensagem enviada para {user}!")
        except discord.Forbidden:
            await ctx.send("Não foi possível enviar DM para esse usuário (possivelmente DMs desativadas).")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Desligando o bot... 👋")
        await commands.close()

async def setup(bot):
    await bot.add_cog(Fun(bot))
