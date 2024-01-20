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

# set intents that the bot will see to "all"
intents = discord.Intents.all()
intents.typing = False

# set the unique symbol to be used with commands
bot = commands.Bot(command_prefix='/', intents=intents)

conn = mysql.connector.connect(host="...", user='root', password="...*", database="...")
conn.autocommit = True
c = conn.cursor(buffered=True)

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


# Example of how to simulate bot typing
@bot.command(name="st") # Change command name to "st".
async def simulate_typing(ctx, seconds: int = 3):

    # Simulate typing.
    async with ctx.typing():
        await asyncio.sleep(seconds)  # Simulate typing for a specified number of seconds.

    # Send a response after simulating typing.
    await ctx.send(f"Finished typing after {seconds} seconds!")


bot.run(config.BOT_TOKEN)
