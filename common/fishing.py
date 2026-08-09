import sqlite3
import discord
from discord.ext import commands
import random
from data.database import get_user_inventory, get_weighted_random_fish, add_fish_to_inventory

def get_prefix(size, base):
    ratio = size / base
    sizes = [
        (0.2, " microscópico"),
        (0.5, " minúsculo"),
        (1, " pequeno"),
        (1.5, ""),
        (1.75, " grande"),
        (2.25, " enorme"),
        (2.75, " massivo"),
        (3.25, " gigantesco"),
    ]
    
    star_weights = [
    (0, 60.0),
    (1, 24.0),
    (2, 11.0),
    (3, 4.0),
    (4, 0.8),
    (5, 0.2),
  ]

    
    for ceiling, prefix in sizes:
        if ratio <= ceiling:
            return prefix
    return "colossal"

class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='fih', aliases=['fish', 'pescar', 'pesca', 'fig', 'pexe'], help='Pesque um peixe!')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self, ctx):
        fish = get_weighted_random_fish()
        fish_name = fish[1]
        fish_description = fish[5]
        average_size = fish[4]
        fish_random_size = max(0.01, random.gauss(1.25 * average_size, 0.55 * average_size))
        fish_stars = random.choices([0, 1, 2, 3, 4, 5], weights=[60.0, 24.0, 11.0, 4.0, 0.8, 0.2])[0]
        stars_prefix = "⭐" * fish_stars
        
        fish_size_prefix = get_prefix(fish_random_size, average_size)
        
        add_fish_to_inventory(ctx.author.id, fish[0], fish_random_size, fish_stars)
        await ctx.send(f"Você pegou um(a) {stars_prefix} {fish_name}{fish_size_prefix} de {fish_random_size:.2f}cm!\n{fish_description}")
        
    class InventoryView(discord.ui.View):
        def __init__(self, author, items, per_page=20):
            super().__init__(timeout=60)
            self.author = author
            self.items = items
            self.per_page = per_page
            self.current_page = 0
            self.total_pages = (len(items) - 1) // per_page + 1
            self.message = None
            self.update_buttons()
            
        def get_page_content(self):
            start = self.current_page * self.per_page
            end = start + self.per_page
            page_items = self.items[start:end]
            
            msg = f"{self.author.mention}-chan, seus peixes (página {self.current_page + 1}/{self.total_pages}):\n"
            msg += "```\n"
            
            for index, (_, fish_name, size, stars) in enumerate(page_items, start=start + 1):
                stars_prefix = "★" * stars
                msg += f"{index}.{fish_name:<15} {size:>6.2f}cm  {stars_prefix}\n"
            
            msg += "```"
            return msg
        
        def update_buttons(self):
            self.prev_page.disabled = self.current_page == 0
            self.next_page.disabled = self.current_page == self.total_pages - 1
            
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("Esse inventário não é teu, filho")
                return False
            return True
        
        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
        async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(content=self.get_page_content(), view=self)

        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
        async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(content=self.get_page_content(), view=self)
            
        async def on_timeout(self):
            for child in self.children:
                child.disabled = True
            try:
                await self.message.edit(view=self)
            except Exception:
                pass
      
    @commands.command(name='inventory', aliases=['inv'], help='Mostra o inventário de peixes do usuário.')
    async def inventory(self, ctx):
        inventory_items = get_user_inventory(ctx.author.id)

        if not inventory_items:
            await ctx.send(f"{ctx.author.mention}-chan, Você não pescou nada!.")
            return

        view = self.InventoryView(ctx.author, inventory_items, per_page=20)
        view.message = await ctx.send(content=view.get_page_content(), view = view)
        
        
    @commands.command(name='soltar', aliases=['release', 'solta', 'oltar', 'olta', 'tchau', 'bye'], help='Solte um peixe do seu inventário.')
    async def release(self, ctx, fish_index: int):
        inventory_items = get_user_inventory(ctx.author.id)

        if fish_index < 1 or fish_index > len(inventory_items):
            await ctx.send(f"{ctx.author.mention}-chan, você não tem esse peixe no seu inventário.")
            return

        fish_to_release = inventory_items[fish_index - 1]
        
        # Como o fish_id agora é o primeiro no SELECT, ele é o índice [0]
        actual_fish_id = fish_to_release[0] 

        connection = sqlite3.connect('data/database.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM inventory WHERE user_id = ? AND fish_id = ?', (ctx.author.id, actual_fish_id))
        connection.commit()
        connection.close()

        # O nome do peixe agora é o índice [1]
        await ctx.send(f"{ctx.author.mention}-chan, você soltou o(a) {fish_to_release[1]} do seu inventário.")
        
    @commands.command(name='soltarlucio', aliases=['release_lucio'], help='Solte todos os Lúcios do seu inventário.')
    async def release_lucio(self, ctx):
        connection = sqlite3.connect('data/database.db')
        cursor = connection.cursor()

        # O SQL agora busca qual é o ID do 'Lúcio' na tabela fishes e deleta as ocorrências na inventory
        cursor.execute('''
            DELETE FROM inventory 
            WHERE user_id = ? 
            AND fish_id = (SELECT id FROM fishes WHERE name = 'Lúcio')
        ''', (ctx.author.id,))
        
        connection.commit()
        connection.close()

        await ctx.send(f"{ctx.author.mention}-chan, você soltou todos os Lúcios do seu inventário.")

    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"...Mas ninguém veio.\n Porém eu sei que um peixe virá em {error.retry_after:.1f} segundos.")
            
async def setup(bot):
    await bot.add_cog(Fishing(bot))
