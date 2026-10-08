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

    def is_ticket(self, channel):
        return channel.topic and "ticket for" in channel.topic.lower()

    @app_commands.command(name="close", description="Close the current ticket")
    @app_commands.describe(reason="Reason for closing")
    async def close_slash(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        if not self.is_ticket(interaction.channel):
            return await interaction.response.send_message("This is not a ticket.")
        
        await interaction.response.send_message(f"Ticket closed by {interaction.user.mention}\nReason: {reason}")
        await interaction.channel.delete(reason=f"Closed by {interaction.user} | {reason}")

    @commands.command(name="close")
    async def close_prefix(self, ctx, *, reason: str = "No reason provided"):
        if not self.is_ticket(ctx.channel):
            return await ctx.send("This is not a ticket.")
        
        await ctx.send(f"Ticket closed by {ctx.author.mention}\nReason: {reason}")
        await ctx.channel.delete(reason=f"Closed by {ctx.author} | {reason}")

    @app_commands.command(name="claim", description="Claim this ticket")
    async def claim(self, interaction: discord.Interaction):
        if not self.is_ticket(interaction.channel):
            return await interaction.response.send_message("This is not a ticket.")
        
        await interaction.channel.send(f"{interaction.user.mention} has claimed this ticket.")
        await interaction.response.send_message("You claimed the ticket.", ephemeral=True)

    @app_commands.command(name="add", description="Add a user to the ticket")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        if not self.is_ticket(interaction.channel):
            return await interaction.response.send_message("This is not a ticket.")
        
        await interaction.channel.set_permissions(user, view_channel=True, send_messages=True)
        await interaction.response.send_message(f"Added {user.mention} to the ticket.")

    @app_commands.command(name="remove", description="Remove a user from the ticket")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        if not self.is_ticket(interaction.channel):
            return await interaction.response.send_message("This is not a ticket.")
        
        await interaction.channel.set_permissions(user, overwrite=None)
        await interaction.response.send_message(f"Removed {user.mention} from the ticket.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
