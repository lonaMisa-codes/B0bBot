import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

class SellModal(Modal, title="Sell Spawners"):
    amount = TextInput(label="Amount of spawners", placeholder="e.g. 5", required=True)
    price = TextInput(label="Price per spawner", placeholder="e.g. 2000", required=True)
    spawner_type = TextInput(label="Spawner Type", placeholder="e.g. iron, gold, diamond", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        config = load_config()
        try:
            amount = int(self.amount.value)
            price = int(self.price.value)
            total = amount * price
            stype = self.spawner_type.value.lower()
        except ValueError:
            return await interaction.response.send_message("Amount and price must be numbers!", ephemeral=True)

        # Create ticket
        guild = interaction.guild
        category = guild.get_channel(config["ticket_category_id"]) if config["ticket_category_id"] else None
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        
        if config["seller_role_id"]:
            role = guild.get_role(config["seller_role_id"])
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        ticket_name = f"sell-{interaction.user.name}"[:100]
        channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites,
            topic=f"Sell ticket for {interaction.user.id}"
        )

        seller_role = f"<@&{config['seller_role_id']}>" if config["seller_role_id"] else "@Seller"
        msg = config["messages"]["sell_ping"].format(
            seller_role=seller_role,
            opener=interaction.user.mention,
            amount=amount,
            type=stype,
            total=f"{total:,}",
            price=f"{price:,}"
        )

        embed = discord.Embed(
            title="New Sell Offer",
            description=msg,
            color=int(config["embed_color"], 16)
        )
        embed.set_footer(text=f"Ticket opened by {interaction.user}")
        
        await channel.send(content=msg, embed=embed)
        await interaction.response.send_message(f"Sell ticket created: {channel.mention}", ephemeral=True)

class BuyModal(Modal, title="Buy Spawners"):
    amount = TextInput(label="Amount of spawners", placeholder="e.g. 3", required=True)
    spawner_type = TextInput(label="Spawner Type", placeholder="e.g. iron, gold, diamond", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        config = load_config()
        try:
            amount = int(self.amount.value)
            stype = self.spawner_type.value.lower()
        except ValueError:
            return await interaction.response.send_message("Amount must be a number!", ephemeral=True)

        price = config["buy_prices"].get(stype)
        if price is None:
            return await interaction.response.send_message(
                f"No buy price set for **{stype}**. Ask staff to set it with `/setbuyprice`.", ephemeral=True
            )

        total = amount * price

        # Create ticket
        guild = interaction.guild
        category = guild.get_channel(config["ticket_category_id"]) if config["ticket_category_id"] else None
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        if config["seller_role_id"]:
            role = guild.get_role(config["seller_role_id"])
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        ticket_name = f"buy-{interaction.user.name}"[:100]
        channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites,
            topic=f"Buy ticket for {interaction.user.id}"
        )

        msg = config["messages"]["buy_total"].format(
            opener=interaction.user.mention,
            amount=amount,
            type=stype,
            total=f"{total:,}"
        )

        embed = discord.Embed(
            title="New Buy Request",
            description=msg,
            color=int(config["embed_color"], 16)
        )
        embed.add_field(name="Price each", value=f"{price:,}", inline=True)
        embed.add_field(name="Total", value=f"{total:,}", inline=True)
        embed.set_footer(text=f"Ticket opened by {interaction.user}")

        await channel.send(content=interaction.user.mention, embed=embed)
        await interaction.response.send_message(f"Buy ticket created: {channel.mention}", ephemeral=True)

class SpawnerPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Sell Spawners", style=discord.ButtonStyle.green, custom_id="spawner_sell")
    async def sell_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(SellModal())

    @discord.ui.button(label="Buy Spawners", style=discord.ButtonStyle.blurple, custom_id="spawner_buy")
    async def buy_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(BuyModal())

class Spawner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(SpawnerPanel())  # Persistent view

    @app_commands.command(name="spawnerpanel", description="Post the Sell/Buy spawner panel")
    async def spawnerpanel(self, interaction: discord.Interaction):
        config = load_config()
        # Permission check
        if not (interaction.user.guild_permissions.administrator or 
                any(r.id in config.get("admin_role_ids", []) for r in interaction.user.roles)):
            return await interaction.response.send_message("No permission.", ephemeral=True)

        embed = discord.Embed(
            title=config["messages"]["panel_title"],
            description=config["messages"]["panel_description"],
            color=int(config["embed_color"], 16)
        )
        view = SpawnerPanel()
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Panel posted!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Spawner(bot))
