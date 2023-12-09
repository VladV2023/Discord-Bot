# Important Imports
import config
import discord
import pymongo

# Other Imports
import random

# Time related imports
import asyncio
import datetime

# Imports from imported libraries
from typing import Literal, Optional
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Greedy, Context # or a subclass of yours
from discord import Button, ButtonStyle

# Create a new client and connect to the server
client = pymongo.MongoClient(config.MONGODB_SRV)

# Name of the database
db = client.Test_Data

# set intents that the bot will see to "all"
intents = discord.Intents.all()

# set the unique symbol to be used with commands
bot = commands.Bot(command_prefix='/', intents=intents)

# A function for silumating sleep, call it with (await sim_type(interaction, "number for duration"))
async def sim_type(interaction, duration):
    await interaction.channel.typing()
    await asyncio.sleep(duration)


# Event command that send Bot information if it connected to the server successfuly
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# Event command when a new user joins the server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel("channel ID goes here")
    role_arsenal_channel = bot.get_channel("channel ID goes here")  # Main chat ID

# Version 1
    #Customize your welcome message with a mention to the "role-arsenal" channel
    welcome_message = (
        f"Hello there {member.mention}, welcome to 🐇Peko's Little Den🐇!\n"
        f"We got no roles for you to grab yet, F.\n"
        "Rules page will be created in the future.\n"
        f"Please come to  {role_arsenal_channel.mention} and start chatting with others!"
    )

    await channel.send(welcome_message)

# Version 2
    # embed = discord.Embed(
    #     description=f"Hello **{member.mention}**, \nwelcome to 🐇 Peko's Little Den 🐇!",
    #     color=0xff55ff,
    #     timestamp=datetime.datetime.now(),
    # )
    # embed.set_thumbnail(url=member.avatar.url)

    # await channel.send(embed=embed)



# Unique events that are triggered by a word or a sentance without any "/" symbols ==================================================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "Slice of life":
        await message.channel.send("There one was a wise person, they knew many things, including the sacred knowledge of how to explore.")
    elif message.content == "iori":
        channel = bot.get_channel(1083972457595142175)
        await message.channel.send("Is the Winner!")
    elif message.content == "Alvy":
        channel = bot.get_channel(1083972457595142175) 
        await message.channel.send("Its international Love!")   
    elif message.content == "Finik you are so bad":
        channel = bot.get_channel(1083972457595142175)
        await channel.send("https://media.discordapp.net/attachments/1083972457595142175/1179202081014423632/Evil-Alastor.gif?ex=6578ec84&is=65667784&hm=8c028fd6a2811fd02a242023766a75509b6cf60d440057ba53d425edb60014a0&=")   
        
    await bot.process_commands(message)


# Command to sync and delete globally and in guild(NERY USEFUL)
#======================================================================================================================================

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
    guild = ctx.guild or discord.Object(id=834909616894246972)  # you can use a full discord.Guild as the method accepts a Snowflake
    bot.tree.copy_global_to(guild=guild)

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.", ephemeral=True)


# Tree Slash Commands
#===================================================================================================================================

# Command to say hello to the command invoker
@bot.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""

    await sim_type(interaction, 1)

    await interaction.response.send_message(f'Hi, {interaction.user.mention}', ephemeral=False)


# Tree Context-menu Commands
#===================================================================================================================================

# Show full profile and other information on a "fancier" embed
@bot.tree.context_menu(name="Show Profile Info")
async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
    embed=discord.Embed(title=f"{member}#{member.discriminator}", description=f"ID: {member.id}")
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles if role.name != '@everyone']), inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Report Message
@bot.tree.context_menu(name="Store Message")
async def report_message(interaction: discord.Interaction, message: discord.Message):
    
    # Access the file inside the database Test_Data > server_messages
    db.server_messages.insert_one(
        {
            "Author": message.author.id,
            "Name": message.author.name,
            "Message": message.content,
            "Date": discord.utils.format_dt(message.created_at),
        }
    )
    
    await interaction.response.send_message(f"Message stored.", ephemeral=False)
    
# Context-command to get all of the user-sent messages
@bot.tree.context_menu(name="Retrieve messages")
async def find_sent_messages(interaction: discord.Interaction, member: discord.User = None):
    messages = db.server_messages.find({"Author": member.id})

    if not messages:
        return await interaction.response.send_message("No messages found for the specified member.")
    else:
        messages_combined = "\n".join(f"**Message:** {message['Message']}\n**Date:** {message['Date']}\n" for message in messages)

        embed = discord.Embed(title=f"{member.name}'s Messages", description=messages_combined)
        embed.set_thumbnail(url=member.avatar.url)

        await interaction.response.send_message(embed=embed)

# # Commands activated by "/" followed by command name, NOT "/sync"
# #=================================================================================================================================

# Special command to talk Using This Bot. -- WORKS
@bot.command(name="say") # change command name to "say" for ease of use.
async def say(ctx, *, message):
    # Get the channel you want the message to be sent to by its ID.
    channel = bot.get_channel(1083972457595142175)

    if channel:
        await channel.send(message)
        await ctx.send(f"Message sent to <#{channel}>: {message}")
    else:
        await ctx.send("Invalid channel ID. Please provide a valid channel ID.")


# Simulate *bot is typing* visual.
@bot.command(name="st") # Change command name to "st".
async def simulate_typing(ctx, seconds: int = 3):

    # Simulate typing.
    async with ctx.typing():
        await asyncio.sleep(seconds)  # Simulate typing for a specified number of seconds.

    # Send a response after simulating typing.
    await ctx.send(f"Finished typing after {seconds} seconds!")


# Do a private DM -- WORKS
@bot.command(name="dm") # Change command name to "dm".
async def DM(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    
    await user.send(message)
    await ctx.send(f'Sent a DM to {user.name}: {message}')


# Send a help menu with allowed commands -- WORKS
@bot.command(name="hmenu")
async def menu(ctx):
    # channel = bot.get_channel(1083972457595142175)

    embed = discord.Embed(
        description="Here are some available commands for this bot:\n"
                    "1. Slice of life - will send a short story.\n"
                    "2. Alvy - will send 'Its international love!'\n"
                    "3. (Slash command when typing '/' into message field) Hello - will greet the person that used the command.\n"
                    "4. (Context menu command when right clicking a user) - Will display the full profile and other information in an embed.\n"
                    "5. (Context menu command when right clicking a message) Store message - will store user's message into the database.\n"
                    "6. (Context menu command when right clicking a user) Retrieve messages - will retrieve all user's messages store on the database.\n"
                    "7. /say - say something using the bot.\n"
                    "8. /st - simulate typing.\n"
                    "9. Iori - will send 'Is the Winner!'\n"
                    "10. /dm - will send a private message to a selected user.\n"
                    "11. /hmenu - will display a fancy list of all functional commands.\n",
        color=0xCF5055,
        #timestamp=datetime.datetime.now()
    )

    await ctx.send(embed=embed)


bot.run(config.BOT_TOKEN)