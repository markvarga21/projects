import discord
import random
import asyncio
import json
import os
import re
import sys
import youtube_dl
import urllib.request
from datetime import date
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get

SERVER_ID = 842848980164411402

os.chdir(r'/home/mark/dcbot/source') # raw string to the project file

class ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    EXPERIENCE_CNT = 5
    # on message event
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await update_data(users, message.author)
            await add_experience(users, message.author, EXPERIENCE_CNT)
            await level_up(users, message.author, message)

            with open('users.json', 'w') as f:
                json.dump(users, f)

        await self.bot.process_commands(message)


    # updating data
    def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1

    # adding experiences
    def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp

    # adding levels
    async def level_up(self, users, user, message):
        with open('levels.json', 'r') as g:
            levels = json.load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            await message.channel.send(f'{user.mention}, a **{lvl_end}**. szintre lépett, gratulálunk!')
            users[f'{user.id}']['level'] = lvl_end

    # displaying level with command
    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        if not member:
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            experience = users[str(id)]['experience']
            await ctx.send(f'A **{lvl}. szinten** vagy, **{experience}** tapasztalatal!')
        else:
            id = member.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            exp = users[str(id)]['experience']
            await ctx.send(f'*{member}* a **{lvl}**. szinten van, **{exp}** tapasztalattal!') # debuggolni a masik emberre valo lekerdezest

def setup(bot):
    bot.add_cog(ranks(bot))