import discord
from discord.ext import commands
from discord import app_commands

class SlashCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # normal command
    @commands.command(name="command")
    async def my_command(self, ctx):
        await ctx.send('This is my command!')


    # Background task to delete messages
    async def background_clear(self, channel, amount):
        try:
            # Delete messages
            deleted_messages = await channel.purge(limit=amount)

            # Send a confirmation message after deletion
            print(f"Cleared {len(deleted_messages)} messages.")

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

    
def setup(bot):
    bot.add_cog(SlashCommandsCog(bot))
