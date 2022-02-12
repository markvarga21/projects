import discord
import random
import asyncio
import json
import os
from discord.ext import commands
from discord.utils import get

os.chdir(r'/home/mark/dcbot') # raw string to the project file

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

############################## BOT'S STATE ###########################

# ready checker
@bot.event 
async def on_ready():
	print('Bot is ready!')

# on member join trigger
@bot.event
async def on_member_join(member):
	# ranking file frissitese joinolas eseten
	with open('users.json', 'r') as f: # olvasasra megnyitja, 'f' temporary variable
		users = json.load(f) 

	await update_data(users, member) # updating data with a helper function

	with open('users.json', 'w') as f: # irasra megnyitja
		json.dump(users, f) # felulirja


	# default role kiosztasa
	guild = bot.get_guild(SERVER_ID) #guild == server
	role = get(member.guild.roles, name=DEFAULT_ROLE) #vegigmegy a szerver role-jain, role object
	await member.add_roles(role)

	# udvozlo uzenet
	channel = guild.get_channel(int(WELCOME_CHANNEL_ID))
	await channel.send(f'Üdvözöllek a **{guild.name}** szerveren, {member.mention}! :partying_face:\n{WELCOME_ROLE_CHOOSE}') #welcome the member on the server
	#privat uzenet kuldes-e a szemelynek: await member.send(f'Udv itt, {member.name}') #this will welcome the member on a DM

################################## USEFUL COMMANDS #############################

# clear command only for admins, clearing the most frecvent messages, it works with and without ammount too
@bot.command()
async def clear(ctx, amount=5):

	user = ctx.message.author # uzenet iroja
	admin_role = get(ctx.guild.roles, name=ADMIN_ROLE)

	if admin_role in user.roles:
		await ctx.channel.purge(limit=amount)
	else:
		await ctx.send('Nincs jogod ezt a parancsot hasznalni!') # ezeket kene torolni egy ido utan valahogy

################################# LITTLE GAMES ########################

# ping test
@bot.command()
async def ping(context): #function name == command name
	await context.send(f'Pong! {round(bot.latency*1000)}ms') #latency in seconds

# 8ball thingy
@bot.command(aliases=['8ball', 'test', '8labda']) #az osszes alias string hasznalhato erre mint alias
async def _8ball_(context, *, question):
	reponses = ['It is certain.', 'Without a doubt!']
	await context.send(f'Question: {question}\nAnswer: {random.choice(reponses)}')

################### ROLE ASSIGNMENT FOR USERS ONLY ###############################

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

########################## LEVEL UPPING/RANKING SYSTEM ######################

EXPERIENCE_CNT = 5
# on message event
@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, EXPERIENCE_CNT)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)

# updating data
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1

# adding experiences
async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

# adding levels
async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention}, a **{lvl_end}**. szintre lépett, gratulálunk!')
        users[f'{user.id}']['level'] = lvl_end

# displaying level with command
@bot.command()
async def rank(ctx, member: discord.Member = None):
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

# running the bot with the given token
bot.run(TOKEN)
