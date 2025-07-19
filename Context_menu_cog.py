import discord

import mysql.connector

from discord.ext import commands
from discord import app_commands


class ContextMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.conn = mysql.connector.connect(host="", user="", password="", database="")
        self.conn.autocommit = True
        self.c = self.conn.cursor(buffered=True)

        # Get Info command initialization
        self.ctx_menu = app_commands.ContextMenu(
            name='Show Profile Info',
            callback=self.get_user_info,
        )
        self.bot.tree.add_command(self.ctx_menu)
        
        # Store command initialization
        self.ctx_menu = app_commands.ContextMenu(
            name='Store Message',
            callback=self.store_context_menu,
        )
        self.bot.tree.add_command(self.ctx_menu)

        # Retrieve command initialization
        self.ctx_menu = app_commands.ContextMenu(
            name='Retrieve Message',
            callback=self.retrieve_context_menu,
        )
        self.bot.tree.add_command(self.ctx_menu)


    # Show full profile and other information on a "fancier" embed
    async def get_user_info(self, interaction: discord.Interaction, member: discord.Member):
        embed=discord.Embed(title=f"{member}#{member.discriminator}", description=f"ID: {member.id}")
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles if role.name != '@everyone']), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    # 'Context Menu Command' to save user-sent message to the database
    async def store_context_menu(self, interaction: discord.Interaction, message: discord.Message) -> None:
        try:
            # Get id of the user who invoked the command
            sender = str(message.author.id)
            print(f"Sender id = {sender}")

            # Formatted date of the message
            formatted_date = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

            # Insert the message into the database
            self.c.execute("INSERT INTO accounts (message, some_date, userid, username) VALUES (%s, %s, %s, %s)", (message.content, formatted_date, sender, message.author.name))
            self.conn.commit()

            await interaction.response.send_message(f"Message stored.", delete_after=2, ephemeral=True)

        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred during message storage: {e}")
            await interaction.response.send_message("An error occurred while processing the command.", ephemeral=True)


    # 'Context Menu Command' to retrieve messages from the database
    async def retrieve_context_menu(self, interaction: discord.Interaction, member: discord.User = None):

        try:    
            # Get id of the user who's profile was clicked on'
            sender_id = str(member.id)
            sender_name = member.name
            print(sender_name)

            # Retrieve messages from the database for the specified member
            self.c.execute("SELECT message, some_date FROM accounts WHERE userid=%s AND username=%s", (sender_id, sender_name))
            messages = self.c.fetchall()

            if not messages:
                return await interaction.response.send_message("No messages found for the specified member.")

            messages_combined = "\n".join(f"**Message:** {message[0]}\n**Date:** {message[1]}\n" for message in messages)

            embed = discord.Embed(title=f"{member.name}'s Messages", description=messages_combined)
            embed.set_thumbnail(url=member.avatar.url)

            await interaction.response.send_message(embed=embed)
    
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred during message retrieval: {e}")
            await interaction.response.send_message("An error occurred while processing the command.", ephemeral=True)


def setup(bot):
    bot.add_cog(ContextMenuCog(bot))

   

    
    
