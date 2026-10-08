import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Shows all bot commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="B0bBot Help",
            description="List of all commands",
            color=0x5865F2
        )

        embed.add_field(
            name="General",
            value=(
                "`/help` - Shows this message\n"
                "`/calc <expression>` - Calculator (Everyone)"
            ),
            inline=False
        )

        embed.add_field(
            name="Tickets",
            value=(
                "`/spawnerpanel` - Post Sell/Buy panel (Admin)\n"
                "`/close` - Close current ticket (Everyone in ticket)\n"
                "`/add <user>` - Add user to ticket\n"
                "`/remove <user>` - Remove user from ticket"
            ),
            inline=False
        )

        embed.add_field(
            name="Moderation",
            value=(
                "`/ban <user> [reason]` - Ban a member (Mod/Admin)\n"
                "`/kick <user> [reason]` - Kick a member (Mod/Admin)\n"
                "`/timeout <user> <minutes> [reason]` - Timeout (Mod/Admin)\n"
                "`/purge <amount>` - Delete messages (Mod/Admin)\n"
                "`/lock` - Lock channel (Mod/Admin)\n"
                "`/unlock` - Unlock channel (Mod/Admin)"
            ),
            inline=False
        )

        embed.add_field(
            name="Admin / Config",
            value=(
                "`/setup` - Setup guide (Admin)\n"
                "`/setcategory` - Set ticket category (Admin)\n"
                "`/setrole` - Set important roles (Admin)\n"
                "`/setlogchannel` - Set log channel (Admin)\n"
                "`/setbuyprice` - Set buy prices (Admin)\n"
                "`/config` - View current config (Admin)"
            ),
            inline=False
        )

        embed.add_field(
            name="Reaction Roles",
            value=(
                "`/rr_add <message_id> <emoji> <role>` - Add reaction role (Admin)\n"
                "`/rr_remove <message_id> <emoji>` - Remove reaction role (Admin)"
            ),
            inline=False
        )

        embed.set_footer(text="Admin = Administrator or roles set with /setrole")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
