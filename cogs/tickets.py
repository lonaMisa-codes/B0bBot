import discord
from discord import app_commands
from discord.ext import commands
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="close", description="Close the current ticket")
    async def close(self, interaction: discord.Interaction):
        if not interaction.channel.topic or "ticket for" not in interaction.channel.topic.lower():
            return await interaction.response.send_message("This is not a ticket channel.", ephemeral=True)

        await interaction.response.send_message("Closing ticket in 3 seconds...")
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")

    @app_commands.command(name="add", description="Add a user to the ticket")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.channel.set_permissions(user, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"Added {user.mention} to the ticket.")

    @app_commands.command(name="remove", description="Remove a user from the ticket")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.channel.set_permissions(user, overwrite=None)
        await interaction.response.send_message(f"Removed {user.mention} from the ticket.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
