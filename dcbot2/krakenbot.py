import discord
import random
import asyncio
from discord.ext import commands
from discord.utils import get


# intents
intents = discord.Intents.default() #let us know who joins the server
intents.members = True

# bot informations
bot = commands.Bot(command_prefix = '.', intents=intents)
TOKEN = "ODQzMDI0NDk4MDAxNTc1OTM3.YJ91vg.5DOsbgoEdqf5DRdXvjyJblvCFz8"

# roles
DEFAULT_ROLE = 'NoRole'
ADMIN_ROLE = 'ADMIN'
TAG_ROLE = 'Tag'
OTHER_ROLES = ['PTI', 'MI', 'GI']

# server and channel ID's
SERVER_ID = 842848980164411402
WELCOME_CHANNEL_ID = 843045778913624074

# Welcome szoveg az atlathatosag kedveert
WELCOME_ROLE_CHOOSE = """Kérlek add meg melyik karról jössz: \n 
	**.PTI** - programtervezo informatikus\n
	**.GI** - gazdasag informatikus\n
	**.MI** - mernok informatikus"""

# ready checker
@bot.event 
async def on_ready():
	print('Bot is ready!')

# on member join trigger
@bot.event
async def on_member_join(member):
	guild = bot.get_guild(SERVER_ID) #guild == server
	role = get(member.guild.roles, name=DEFAULT_ROLE) #vegigmegy a szerver role-jain, role object
	await member.add_roles(role)
	channel = guild.get_channel(int(WELCOME_CHANNEL_ID))
	await channel.send(f'Üdvözöllek a **{guild.name}** szerveren, {member.mention}! :partying_face:\n{WELCOME_ROLE_CHOOSE}') #welcome the member on the server
	#privat uzenet kuldes-e a szemelynek: await member.send(f'Udv itt, {member.name}') #this will welcome the member on a DM

# clear command only for admins, clearing the most frecvent messages, it works with and without ammount too
@bot.command()
async def clear(ctx, amount=5):

	user = ctx.message.author # uzenet iroja
	admin_role = get(ctx.guild.roles, name=ADMIN_ROLE)

	if admin_role in user.roles:
		await ctx.channel.purge(limit=amount)
	else:
		await ctx.send('Nincs jogod ezt a parancsot hasznalni!') # ezeket kene torolni egy ido utan valahogy

# ping test
@bot.command()
async def ping(context): #function name == command name
	await context.send(f'Pong! {round(bot.latency*1000)}ms') #latency in seconds

# 8ball thingy
@bot.command(aliases=['8ball', 'test', '8labda']) #az osszes alias string hasznalhato erre mint alias
async def _8ball_(context, *, question):
	reponses = ['It is certain.', 'Without a doubt!']
	await context.send(f'Question: {question}\nAnswer: {random.choice(reponses)}')

# PTI role maker
@bot.command(aliases=['pti'])
async def PTI(ctx):

	user = ctx.message.author # uzenet iroja
	def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

	if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
		role = get(ctx.guild.roles, name=OTHER_ROLES[0]) # PTI role kinyerese 
		await user.add_roles(role) # PTI role hozzaadasa
		await user.remove_roles(def_role) # NoRole role elvetele
		tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
		await user.add_roles(tagsagi) # tagsagi role hozzaadasa
	else:
		await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak

# GI role maker
@bot.command(aliases=['gi'])
async def GI(ctx):

	user = ctx.message.author # uzenet iroja
	def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

	if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
		role = get(ctx.guild.roles, name=OTHER_ROLES[2]) # PTI role kinyerese 
		await user.add_roles(role) # PTI role hozzaadasa
		await user.remove_roles(def_role) # NoRole role elvetele
		tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
		await user.add_roles(tagsagi) # tagsagi role hozzaadasa
	else:
		await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak

# MI role maker
@bot.command(aliases=['mi'])
async def MI(ctx):

	user = ctx.message.author # uzenet iroja
	def_role = get(ctx.guild.roles, name=DEFAULT_ROLE) # NoRole megkeresese a server role-k kozott

	if def_role in user.roles: # benne van-e a user role-jai kozott a def_role vagyis a NoRole
		role = get(ctx.guild.roles, name=OTHER_ROLES[1]) # PTI role kinyerese 
		await user.add_roles(role) # PTI role hozzaadasa
		await user.remove_roles(def_role) # NoRole role elvetele
		tagsagi = get(ctx.guild.roles, name=TAG_ROLE)
		await user.add_roles(tagsagi) # tagsagi role hozzaadasa
	else:
		await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak

# running the bot with the given token
bot.run(TOKEN)
