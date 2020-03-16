import os
import sys
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(dotenv_path="./env")
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX")
#print(TOKEN)
#print(PREFIX)

BadWords = ["penis", "dick", "d1ck", "pik", "pikhoved", "pnis", "fuck", "fucking", "fucker", "nigger", "nigga", "niggar", "negger", "negga", "neggar", "negrow", "negro",
"nignog", "nignag", "fandme", "dumbass", "luder", "ludder", "gay","gai", "bøsse", "bitch", "bich", "svin", "kælling", "helvede"]

Marking = []

client = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)


@bot.command(
    name = "mark",
    help = "Viser at du gerne vil sige noget"
)
async def mark(ctx):
    if ctx.author.display_name in Marking:
        print("Already in array")
        await ctx.channel.send("Du er allerede i køen!", delete_after=2)
    else:
        Marking.append(ctx.author.display_name)
        print(ctx.author.display_name + " has been added\n")
    

@bot.command(
    name = "showline",
    help = "This show the line of people in Marking"
)
@commands.has_role("Lærer")
async def showline(ctx):
    channel = bot.get_channel(688030493467476038)
    if len(Marking) > 0:
        line = ""
        for us in Marking:
            line += us + "\n"
        await channel.send("Køen er: \n" + line + "\n")
    else:
        await channel.send("Køen er tom")


@bot.command(
   name = "unmark",
   help = "Afmarkere dig fra listen"
)
async def unmark(ctx):
    for us in Marking:
        if us == ctx.author.display_name:
            Marking.remove(us)
            print(ctx.author.display_name + " has been removed\n")
            break


@bot.command(
    name = "fartmode",
    help = "Fartmode activated"
)
async def fartmode(ctx):
    await ctx.channel.send("Bot is now in fartmode!")
    with open('img/fartmode.png', 'rb') as f:
        picture = discord.File(f)
    await ctx.channel.send(file=picture)

    await ctx.guild.me.edit(nick="Fartmode")
    print(type(ctx.guild.me.roles))
    currolle = ctx.guild.me.roles[ctx.guild.me.roles.index("Test Admin")]
    print(currolle)
    print(ctx.guild.me.roles)


@bot.command(
    name = "resetNick",
    help = "Nulstil kælenavnet"
)
async def resetNick(ctx):
    await ctx.guild.me.edit(nick="Test bot")


@bot.command(
    name = "kill"
)
async def kill(ctx):
    if ctx.author.id == 412726759809613836 or ctx.author.id == 199571070246715393 or ctx.author.id == 213676559259795456:
        await ctx.send("Stopping bot...")
        await bot.logout()
    else:
        await ctx.send(ctx.author.mention + ", men dont try turn me off you mother you")


@bot.event
async def on_message(message):
    msg = message.content.lower()
    for BW in BadWords:
        if BW in msg:        
            await message.delete()
            await message.channel.send("No swearing!", delete_after=2)
            break

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'They are connetced to the following guild(s):')
    for guild in bot.guilds:
        print(f'{guild.name} (id:{guild.id})')

bot.run(TOKEN)
