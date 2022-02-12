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


# roles
DEFAULT_ROLE = 'NoRole'
ADMIN_ROLE = 'ADMIN'
TAG_ROLE = 'Tag'
OTHER_ROLES = ['PTI', 'MI', 'GI']

# server and channel ID's
SERVER_ID = 842848980164411402
WELCOME_CHANNEL_ID = 843045778913624074

DELETE_AFTER_REPLY_TIME = 10 # in seconds

class welcome_autorole(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# PTI role maker
	@commands.command(aliases=['pti'])
	async def PTI(self, ctx):

		user = ctx.message.author # uzenet iroja
		def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

		if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
			role = get(ctx.guild.roles, name=OTHER_ROLES[0]) # PTI role kinyerese 
			await user.add_roles(role) # PTI role hozzaadasa
			await user.remove_roles(def_role) # NoRole role elvetele
			tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
			await user.add_roles(tagsagi) # tagsagi role hozzaadasa
		else:
			msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
			await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
			await msg.delete() # deleting message

	# GI role maker
	@commands.command(aliases=['gi'])
	async def GI(self, ctx):

		user = ctx.message.author # uzenet iroja
		def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

		if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
			role = get(ctx.guild.roles, name=OTHER_ROLES[2]) # PTI role kinyerese 
			await user.add_roles(role) # PTI role hozzaadasa
			await user.remove_roles(def_role) # NoRole role elvetele
			tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
			await user.add_roles(tagsagi) # tagsagi role hozzaadasa
		else:
			msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
			await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
			await msg.delete() # deleting message

	# MI role maker
	@commands.command(aliases=['mi'])
	async def MI(self, ctx):

		user = ctx.message.author # uzenet iroja
		def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

		if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
			role = get(ctx.guild.roles, name=OTHER_ROLES[1]) # PTI role kinyerese 
			await user.add_roles(role) # PTI role hozzaadasa
			await user.remove_roles(def_role) # NoRole role elvetele
			tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
			await user.add_roles(tagsagi) # tagsagi role hozzaadasa
		else:
			msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
			await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
			await msg.delete() # deleting message

def setup(bot):
	bot.add_cog(welcome_autorole(bot))