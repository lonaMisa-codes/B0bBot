import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Shows all commands")
    async def help_slash(self, interaction: discord.Interaction):
        await self.send_help(interaction)

    @commands.command(name="help")
    async def help_prefix(self, ctx):
        await self.send_help(ctx)

    async def send_help(self, ctx_or_interaction):
        embed = discord.Embed(
            title="B0bBot Commands",
            description="Both `/` slash and `!` prefix work",
            color=0x5865F2
        )

        embed.add_field(
            name="General",
            value="`/help` or `!help`\n`/ping` or `!ping`\n`/calc <math>` or `!calc <math>`",
            inline=False
        )

        embed.add_field(
            name="Tickets",
            value=(
                "`/spawnerpanel` - Sell/Buy panel (Admin)\n"
                "`/ticketpanel` - Normal support panel (Admin)\n"
                "`/close [reason]` - Close ticket\n"
                "`/add <user>` - Add user to ticket\n"
                "`/remove <user>` - Remove user\n"
                "`/claim` - Claim the ticket"
            ),
            inline=False
        )

        embed.add_field(
            name="Moderation",
            value="`/ban` `/kick` `/timeout` `/purge` `/lock` `/unlock`",
            inline=False
        )

        embed.add_field(
            name="Admin",
            value="`/setup` `/setcategory` `/setrole` `/setbuyprice` `/config`",
            inline=False
        )

        embed.set_footer(text="Made with ❤️")
        
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! `{latency}ms`")

    @commands.command(name="ping")
    async def ping_prefix(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! `{latency}ms`")

async def setup(bot):
    await bot.add_cog(Help(bot))
