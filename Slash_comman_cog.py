import discord
from discord.ext import commands
from discord import app_commands

class SlashCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Background task to delete messages
    async def background_clear(self, channel, amount):
        try:
            # Delete messages
            deleted_messages = await channel.purge(limit=amount)

            # Send a confirmation message after deletion(to the discord application chat)
            await channel.send(f"Cleared {len(deleted_messages)} messages.", delete_after=2)

            # Send a confirmation message after deletion(to the console)
            print(f"\nCleared {len(deleted_messages)} messages.")

        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred during background clear: {e}")

    @app_commands.command(name='clear')
    @commands.is_owner()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        try:
            # Ensure the amount is between 1 and 100 for safety
            amount = max(1, min(50, amount))

            # Acknowledge the command
            await interaction.response.send_message(f"Clearing {amount} messages in the background.", ephemeral=True)

            # Call and Start a background task to delete messages
            self.bot.loop.create_task(self.background_clear(interaction.channel, amount))

        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")

            # Send an error message to the user
            await interaction.response.send_message("An error occurred while processing the command.", ephemeral=True)

    
    @app_commands.command(name="say") # change command name to "say" for ease of use.
    @commands.is_owner()
    # async def say(interaction: discord.Interaction, message: str, channel_name: str = "main-lobby"):
    async def say(self, interaction: discord.Interaction, message: str, channel_name: discord.TextChannel = None):
        
        #await interaction.response.defer()

        if not channel_name:
            channel_name = discord.utils.get(interaction.guild.channels, name="")

        if channel_name:
            await channel_name.send(message)
            await interaction.response.send_message(f"Sent to #{channel_name}: {message}", delete_after=2, ephemeral=True)
        else:
            await interaction.response.send_message("Invalid channel name. Please provide a valid channel name.")
            

def setup(bot):
    bot.add_cog(SlashCommandsCog(bot))
