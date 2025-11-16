import discord
from discord.ext import commands
import sqlite3
import random

from . import fish_data as fd
from . import db_manager as db

conn = sqlite3.connect('GENERAL_INVENTORY.db')
cursor = conn.cursor()

class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    db.setup_database()
    
   
async def setup(bot):
    await bot.add_cog(Fishing(bot))
