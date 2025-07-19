# Important imports
import config
import discord

# Other Imports
import random

# Time related imports
import asyncio
import datetime

# Connection imports
import mysql.connector

# Imports from imported libraries
from discord.ext.commands import Greedy, Context # or a subclass of yours
from typing import Literal, Optional
from discord.ext import commands

from Slash_command_cog import SlashCommandsCog
from Context_menu_cog import ContextMenuCog
from Normal_command_cog import NormalCommandsCog

# set intents that the bot will see to "all"
intents = discord.Intents.all()
intents.typing = False

# set the unique symbol to be used with commands
bot = commands.Bot(command_prefix='/', intents=intents)


# Event command that send Bot information if it connected to the server successfuly
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} \n')

    # Adding cog inside an asynchronous function
    try:
        await bot.add_cog(SlashCommandsCog(bot))
        print('Successfully added SlashCommandsCog to the bot.')
    except Exception as e:
        print(f'Failed to add SlashCommandsCog to the bot. Error: {e}')

    try:
        await bot.add_cog(ContextMenuCog(bot))
        print('Successfully added ContextMenuCog to the bot.')
    except Exception as e:
        print(f'Failed to add ContextMenuCog to the bot. Error: {e}')
        
    try:
        await bot.add_cog(NormalCommandsCog(bot))
        print('Successfully added NormalCommandsCog to the bot.')
    except Exception as e:
        print(f'Failed to add NormalCommandsCog to the bot. Error: {e}')


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^", "^^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        elif spec == "^^": # once used the bot needs a reboot to re-sync the commands. (destructive command)
            ctx.bot.tree.clear_commands(guild=None)
            await ctx.bot.tree.sync()
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}", ephemeral=True)
        return

    ret = 0
    guild = ctx.guild or discord.Object(id=...)  # you can use a full discord.Guild as the method accepts a Snowflake
    bot.tree.copy_global_to(guild=guild)

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.", ephemeral=True)


# Send something when a word or a phrase is sent to the channel. (WORKS)
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.content == "Slice of life":
        await message.channel.send("There one was a wise person, they knew many things, including the sacred knowledge of how to explore.")
    elif message.content == "iori":
        # channel = bot.get_channel(1083972457595142175)
        await message.channel.send("Is the Winner!")
    elif message.content == "Alvy":
        # channel = bot.get_channel(1083972457595142175) 
        await message.channel.send("Its international Love!")   
    elif message.content == "Finik you are so bad":
        # channel = bot.get_channel(1083972457595142175)
        await message.channel.send("")   


# Send custom message when a new member joins the server. (WORKS)
@bot.event
async def on_member_join(member):
    channel = bot.get_channel()
    role_arsenal_channel = bot.get_channel()  # Trash chat ID


# Version 1
    # Customize your welcome message with a mention to the "role-arsenal" channel
    welcome_message = (
        f"Hello there {member.mention}, welcome to 🐇Peko's Little Den🐇!\n"
        f"We got no roles for you to grab yet, F.\n"
        "Rules page will be created in teh future :p lol.\n"
        f"Please come to  {role_arsenal_channel.mention} and start chatting with others!"
    )

    await channel.send(welcome_message)

bot.run(config.BOT_TOKEN)
