import discord
from discord import app_commands
from discord.ext import commands
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin():
        async def predicate(interaction: discord.Interaction):
            config = load_config()
            if not config["admin_role_ids"]:
                return interaction.user.guild_permissions.administrator
            return any(role.id in config["admin_role_ids"] for role in interaction.user.roles)
        return app_commands.check(predicate)

    @app_commands.command(name="setup", description="Initial setup of the bot")
    @is_admin()
    async def setup(self, interaction: discord.Interaction):
        config = load_config()
        embed = discord.Embed(
            title="Bot Setup",
            description="Use the commands below to configure everything:\n\n"
                        "`/setcategory` - Set ticket category\n"
                        "`/setrole` - Set Seller / Buy Price / Admin roles\n"
                        "`/setlogchannel` - Set log channel\n"
                        "`/setbuyprice` - Set buy prices\n"
                        "`/spawnerpanel` - Post the Sell/Buy panel\n"
                        "`/config` - View current config",
            color=int(config["embed_color"], 16)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="setcategory", description="Set the ticket category")
    @is_admin()
    async def setcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        config = load_config()
        config["ticket_category_id"] = category.id
        save_config(config)
        await interaction.response.send_message(f"Ticket category set to **{category.name}**", ephemeral=True)

    @app_commands.command(name="setlogchannel", description="Set the log channel")
    @is_admin()
    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = load_config()
        config["log_channel_id"] = channel.id
        save_config(config)
        await interaction.response.send_message(f"Log channel set to {channel.mention}", ephemeral=True)

    @app_commands.command(name="setrole", description="Set important roles")
    @app_commands.describe(role_type="Which role to set", role="The role")
    @app_commands.choices(role_type=[
        app_commands.Choice(name="Seller Role (pinged on sell)", value="seller"),
        app_commands.Choice(name="Buy Price Role (can set prices)", value="buyprice"),
        app_commands.Choice(name="Admin Role", value="admin"),
    ])
    @is_admin()
    async def setrole(self, interaction: discord.Interaction, role_type: str, role: discord.Role):
        config = load_config()
        if role_type == "seller":
            config["seller_role_id"] = role.id
        elif role_type == "buyprice":
            config["buy_price_role_id"] = role.id
        elif role_type == "admin":
            if role.id not in config["admin_role_ids"]:
                config["admin_role_ids"].append(role.id)
        save_config(config)
        await interaction.response.send_message(f"**{role_type}** role set to {role.mention}", ephemeral=True)

    @app_commands.command(name="setbuyprice", description="Set or update buy price for a spawner type")
    @is_admin()
    async def setbuyprice(self, interaction: discord.Interaction, spawner_type: str, price: int):
        config = load_config()
        # Also allow the buy_price_role
        if not (interaction.user.guild_permissions.administrator or 
                any(r.id == config.get("buy_price_role_id") for r in interaction.user.roles) or
                any(r.id in config["admin_role_ids"] for r in interaction.user.roles)):
            return await interaction.response.send_message("You don't have permission.", ephemeral=True)

        config["buy_prices"][spawner_type.lower()] = price
        save_config(config)
        await interaction.response.send_message(f"Buy price for **{spawner_type}** set to **{price}**", ephemeral=True)

    @app_commands.command(name="config", description="View current configuration")
    @is_admin()
    async def config(self, interaction: discord.Interaction):
        config = load_config()
        embed = discord.Embed(title="Current Config", color=int(config["embed_color"], 16))
        embed.add_field(name="Ticket Category ID", value=str(config["ticket_category_id"]), inline=False)
        embed.add_field(name="Log Channel ID", value=str(config["log_channel_id"]), inline=False)
        embed.add_field(name="Seller Role ID", value=str(config["seller_role_id"]), inline=False)
        embed.add_field(name="Buy Price Role ID", value=str(config["buy_price_role_id"]), inline=False)
        embed.add_field(name="Admin Role IDs", value=str(config["admin_role_ids"]), inline=False)
        prices = "\n".join([f"**{k}**: {v}" for k, v in config["buy_prices"].items()]) or "None set"
        embed.add_field(name="Buy Prices", value=prices, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
