import discord
from discord import app_commands
from discord.ext import commands
import json
from datetime import timedelta

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_mod():
        async def predicate(interaction: discord.Interaction):
            config = load_config()
            return (interaction.user.guild_permissions.moderate_members or
                    any(r.id in config.get("admin_role_ids", []) for r in interaction.user.roles))
        return app_commands.check(predicate)

    @app_commands.command(name="ban", description="Ban a member")
    @is_mod()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Banned {member} | Reason: {reason}")

    @app_commands.command(name="kick", description="Kick a member")
    @is_mod()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {member} | Reason: {reason}")

    @app_commands.command(name="timeout", description="Timeout a member")
    @is_mod()
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason"):
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await interaction.response.send_message(f"Timed out {member} for {minutes} minutes | Reason: {reason}")

    @app_commands.command(name="purge", description="Delete messages")
    @is_mod()
    async def purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(name="lock", description="Lock the channel")
    @is_mod()
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("Channel locked.")

    @app_commands.command(name="unlock", description="Unlock the channel")
    @is_mod()
    async def unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message("Channel unlocked.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
