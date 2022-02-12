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

#modules to install: discord.py, pynacl, json?, python3.9, pip3.9, ffmpeg, youtube_dl


os.chdir(r'/home/mark/projects/dcbot') # raw string to the project file

# intents
intents = discord.Intents.default() #let us know who joins the server
intents.members = True

# bot informations
bot = commands.Bot(command_prefix = '!', intents=intents)

secret_filename = 'sec_token.json'
api_keys = {}
with open(secret_filename, 'r') as f:
	api_keys = json.loads(f.read())

TOKEN = api_keys['DC_TOKEN']

# roles
DEFAULT_ROLE = 'NoRole'
ADMIN_ROLE = 'ADMIN'
TAG_ROLE = 'Tag'
OTHER_ROLES = ['PTI', 'MI', 'GI']

# server and channel ID's
SERVER_ID = 842848980164411402
WELCOME_CHANNEL_ID = 843045778913624074
BIRTHDAY_CHANNEL_ID = 843190029991542798

# Welcome szoveg az atlathatosag kedveert
WELCOME_ROLE_CHOOSE = """Kérlek add meg melyik karról jössz: \n 
	**.PTI** - programtervezo informatikus\n
	**.GI** - gazdasag informatikus\n
	**.MI** - mernok informatikus"""

DELETE_AFTER_REPLY_TIME = 10 # in seconds
CLEAR_AMOUNT = 5

# commands
ALL_COMMANDS = """
**!info** - szerver informaciok
**!pong** - erdekes cucc
**!telljoke - vicc mondasa
**!allmembers** - szerveren levo felhasznalok szama
**!8ball** - kerdesre random valasz
**!clear <n>** - a korabbi *n* uzenet torlese
**!myroles** - felhasznalo sajat rangjainak lekerdezese 
**!thankyou** - koszonom parancs, ugy funbol :D
**!tictactoe** *@Jatekos1* *@Jatekos2* - amoba jatek
	**!place <n>** - *n*-ik helyre rakas (szamozas 1-9-ig)
**!rank** - sajat felhasznalo rangja, uzenetekerte lehet tapasztaltot szerezni
	**!rank** *@Szemely1* - Szemely1 rangjanak lekerdezese
**!bday *YYYY.MM.DD* ** - szulinap hozzaadasa, ha megadod felkoszont a szulinapodon :) (formatum: *ev*.*honap*.*nap*)
	**!listbd** - szulinapok listazasa
**!todaydate** - a mai nap datuma
**Music commands:**
	**!join** - Jarvis csatlakozik abba a voice channel-be ahol jelenleg vagy
	**!leave** - Jarvis elhagyja a voice channel-t
	**!play *<zene cime>* **- adott cimmel rendelezo zene lejatszasa
	**!stop** - zenelejatszas megallitasa
	**!pause** - zenelejatszas szuneteltetese
	**!resume** - zenelejatszas folytatasa
"""

# server informations
SZERVER_INFOK = """
Ide valamiket lehet irni
amiket ki fog mutatni a dc
"""

JOKES_ARR = [
"""- Mi van ha elütnek egy matematikust. ?
- Már nem számít.""",
"""- Mért volt szegény Petőfi Sándor?
- ???
- Mert keveset keresett és sokat költött.""",
"""Tegnap betörtek Stahl Judithoz aki ekkor pisztolyt rántott."""
]

############################## BOT'S STATE ###########################

# ready checker
@bot.event 
async def on_ready():
	print('Bot is ready!')
	bday_check.start()

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
	await channel.send(f'Üdvözöllek a **{guild.name}** szerveren, {member.mention}! :partying_face:\nA parancsok listajat itt talalod: **!help**\n{WELCOME_ROLE_CHOOSE}') #welcome the member on the server
	#privat uzenet kuldes-e a szemelynek: await member.send(f'Udv itt, {member.name}') #this will welcome the member on a DM

################################## USEFUL COMMANDS #############################

# telling a random joke
@bot.command()
async def telljoke(ctx):
	await ctx.send(random.choice(JOKES_ARR))


# clear command only for admins, clearing the most frecvent messages, it works with and without ammount too
@bot.command()
async def myroles(ctx):
	rls = ""
	user = ctx.author
	for rl in user.roles:
		if rl != 'everyone':
			rls += f'{rl}, '
	await ctx.send(rls)

@bot.command()
async def clear(ctx, amount=CLEAR_AMOUNT):

	user = ctx.message.author # uzenet iroja
	admin_role = get(ctx.guild.roles, name=ADMIN_ROLE)

	if admin_role in user.roles:
		await ctx.channel.purge(limit=amount)
	else:
		msg = await ctx.send('Nincs jogod ezt a parancsot hasznalni!') # ezeket kene torolni egy ido utan valahogy
		await asyncio.sleep(DELETE_AFTER_REPLY_TIME)
		await msg.delete()

# mennyi ember vna a szerveren
@bot.command(aliases=['emberszam', 'mennyiember'])
async def allmembers(ctx):
	await ctx.send(f'A szerveren osszesen {ctx.guild.member_count} ember van!')

# mennyi online ember van a szerveren




@bot.command()
async def cmd(ctx):
	await ctx.send(f'A szerveren hasznalhato parancsok:{ALL_COMMANDS}')

@bot.command()
async def info(ctx):
	await ctx.send(SZERVER_INFOK)

################################# LITTLE GAMES ########################

# thank you command
@bot.command(aliases=['ty', 'thanks'])
async def thankyou(ctx):
	await ctx.send('You`re very welcome!')

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
		msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
		await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
		await msg.delete() # deleting message

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
		msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
		await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
		await msg.delete() # deleting message

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
		msg = await ctx.send('Nem lehet többször beállítani ugyan azt a role-t!') # ha tobbszor megprobalna ugyan azt a rangot adni maganak
		await asyncio.sleep(DELETE_AFTER_REPLY_TIME) # waiting 10s till delete
		await msg.delete() # deleting message

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
        print(f'end level: {lvl_end}, exp: {exp}, lvl: {lvl}')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        exp = users[str(id)]['experience']
        await ctx.send(f'*{member}* a **{lvl}**. szinten van, **{exp}** tapasztalattal!') # debuggolni a masik emberre valo lekerdezest

##################################### TICTACTOE ###################################################
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

class birthday:
	def __init__(self, name, date):
		self.name = name
		self.date = date
	def __str__(self):
		return "%s | %s" % (self.name, self.date)

BIRTHDAYS = []

################################### BIRTHDAY #######################################
@bot.command()
async def bday(ctx, szoveg2):
	BIRTHDAYS.append( birthday(ctx.author, szoveg2) )

@bot.command()
async def listbd(ctx):
	for bd in BIRTHDAYS:
		await ctx.send(bd)

@tasks.loop(hours=24) # pontosabba kell tenni
async def bday_check():
	today = date.today()
	for bd in BIRTHDAYS:
		curr_date = datetime.strptime(bd.date, '%Y.%m.%d')
		curr_month = curr_date.month
		curr_day = curr_date.day
		if today.month == curr_month and today.day == curr_day:
			guild = bot.get_guild(SERVER_ID)
			channel = guild.get_channel(BIRTHDAY_CHANNEL_ID)
			await channel.send(f'Boldog szulinapot {bd.name.mention}!')

@bot.command()
async def todaydate(ctx):
	today = date.today()
	date2 = datetime.strptime('2019.4.13', '%Y.%m.%d')
	await ctx.send(today)

####################################### MUSIC FEATURES ############################


# EXTRACTING IMAGE

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

@bot.command(name="pic")
async def get_pic(ctx):
    # profile picture
    asset = ctx.author.avatar_url_as(size=64)
    data = BytesIO(await asset.read())
    prof_image = Image.open(data)

    # background image
    w, h = 450, 150
    shape = [(10, 10), (w - 10, h - 20)]

    # creating new Image object
    img = Image.new("RGB", (w, h), color='#22272a')

    # create rectangle image
    img1 = ImageDraw.Draw(img)
    img1.rectangle(shape, fill='black')

    fnt = ImageFont.truetype("/home/mark/dcbot/Cutie Shark.ttf", 40)

    img1.text((150,50), str(ctx.author), font=fnt, fill=(255,255,255,255))

    # pasting
    img.paste(prof_image, (25, 40))
    img.save('kicsikep.jpg')

    await ctx.send(file=discord.File('kicsikep.jpg'))

    os.remove('kicsikep.jpg')

    #print(str(ctx.author))

@bot.command()
async def profpic(message): 
    user = message.guild.get_member(message.author.id) # Fake snowflake, will not work
    if not user:
        return # Can't find the user, then quit
    pfp = user.avatar_url
    #embed=discord.Embed(title="test", description='{}, test'.format(user.mention) , color=0xecce8b)
    #embed.set_image(url=(pfp))
    #await message.send(message.channel, embed=embed)
    print(pfp)

bot.load_extension("music")

# running the bot using the secret token
bot.run(TOKEN)
