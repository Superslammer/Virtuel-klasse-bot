import os
import sys
import time
import discord
from threading import Thread
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(dotenv_path="../.env")
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX")
MUTETIME = 1000

BadWords = ["penis", "dick", "d1ck", "pik", "pikhoved", "pnis", "fuck", "fucking", "fucker", "nigger", "nigga", "niggar", "negger", "negga", "neggar", "negrow", "negro",
"nignog", "nignag", "fandme", "dumbass", "luder", "ludder", "gay","gai", "bøsse", "bitch", "bich", "svin", "kælling", "helvede"]

Marking = []
Warned = {}
MarkingChannel = 693475965636182047 #694256170445045801
MaintenanceChannel = 643419670996844558 #687664303247196240

client = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)


@bot.command(
    name = "mark",
    help = "Viser at du gerne vil sige noget"
)
async def mark(ctx):
    #await ctx.message.delete()
    await marking(ctx, True)


@bot.command(
    name = "unmark",
    help = "Afmarkere dig fra listen"
)
async def unmark(ctx):
    #await ctx.message.delete()
    await marking(ctx, False)

#TODO:
#- spam protect
#- fix the dict, and manipulate it in the rigth way
async def marking(ctx, mark: bool):
    global Warned
    MuteTr = Thread(target = mute)
    if mark:
        if ctx.author.display_name in Marking:
            print("Already in array")
            if Warned.get(ctx.author) == None:
                await ctx.message.delete()
                await ctx.channel.send("Du er allerede i køen!", delete_after=2)
                Warned[ctx.author] = 0
            elif Warned[ctx.author] == 3:
                MuteTr.start()
            else:
                for user in Warned:
                    if user.display_name == ctx.author.display_name:
                        user += 1

        else:
            Marking.append(ctx.author.display_name)
            print(ctx.author.display_name + " has been added")
    else:
        removed = False
        for us in Marking:
            if us == ctx.author.display_name:
                Marking.remove(us)
                print(ctx.author.display_name + " has been removed")
                removed = True
                break
        if not removed:
            await ctx.channel.send("Du er allerede i køen!", delete_after=2)
            
    if MarkingChannel == "undefined":
        ctx.send("Markingchannel ikke defineret. Brug !markingchannel <tekst-kanal id> for at definere kanal")
        return
    try:
        channel = bot.get_channel(MarkingChannel)
    except:
        ctx.send("Kunne ikke finde kanalen. Brug !markingchannel <tekst-kanal id> for at definere kanal")
        return
    msg = await channel.history(limit = 2).flatten()
    if len(Marking) > 0:
        if "Køen er[" in msg[0].content:
            await msg[0].edit(content = generateline())
        elif "Køen er tom" in msg[0].content:
            await msg[0].edit(content = generateline())
        else:
            await channel.send(generateline())
    elif "Køen er[" in msg[0].content or "Køen er tom" in msg[0].content:
        await msg[0].edit(content = "Køen er tom")
    else:
        await channel.send("Køen er tom")


@bot.command(
    name = "printMute"
)
async def printMute(ctx):
    print(Warned)


def mute():
    time.sleep(5)
    print("Unmute")


@bot.command(
    name = "resetmark",
    help = "Nulstiller håndsoprækningskøen"
)
async def resetmark(ctx):
    channel = bot.get_channel(MarkingChannel)
    roles = []
    for role in ctx.author.roles:
        roles.append(role.name)
    
    if "Lærer" in roles or "Moderator" in roles:
        Marking.clear()
        msg = await channel.history(limit = 2).flatten()
        await msg[0].edit(content = "Køen er tom")
        print("Array cleared")


def generateline():
    line = f"Køen er[{len(Marking)}]: \n"
    for us in Marking:
            line += us + "\n"
    return line


@bot.command(
    name = "markingchannel",
    help = "Bestemmer hvilken tekstkanal som botten skal skrive køen i"
)
@commands.has_role("Moderator")
async def markingchannel(ctx, channel: int):
    global MarkingChannel
    MarkingChannel = channel


@bot.command(
    name = "kill"
)
async def kill(ctx):
    channel = bot.get_channel(MaintenanceChannel)
    msg = await bot.get_channel(MarkingChannel).history(limit = 2).flatten()
    if ctx.author.id == 412726759809613836 or ctx.author.id == 199571070246715393 : # or ctx.author.id == 213676559259795456:
        print("Shutting down bot...")
        await channel.send("Stopping bot...")
        await msg[0].edit(content = "Køen er tom")
        await bot.logout()
    else:
        await ctx.send(ctx.author.mention + ", men dont try turn me off you mother you", delete_after=2)


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
    print()
    print("--------------------------------------------------")
    print(f'{bot.user.name} has connected to Discord!')
    print(f'They are connetced to the following guild(s):')
    for guild in bot.guilds:
        print(f'{guild.name} (id:{guild.id})')
    print("--------------------------------------------------")


bot.run(TOKEN)