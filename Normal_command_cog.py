import discord
from discord.ext import commands
from discord import app_commands

class NormalCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Send a help menu with allowed commands -- WORKS
    @commands.command(name="hmenu")
    async def menu(self, ctx):
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


    # Do a private DM -- WORKS
    @commands.command(name="dm") # Change command name to "dm".
    async def DM(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is sent via DM"
        
        channel = #Id here

        await user.send(message)
        await ctx.channel.send(f'Sent a DM to {user.name}: {message}')


def setup(bot):
    bot.add_cog(NormalCommandsCog(bot))
