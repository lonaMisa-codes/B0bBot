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

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin():
        async def predicate(interaction: discord.Interaction):
            config = load_config()
            return (interaction.user.guild_permissions.administrator or
                    any(r.id in config.get("admin_role_ids", []) for r in interaction.user.roles))
        return app_commands.check(predicate)

    @app_commands.command(name="rr_add", description="Add reaction role to a message")
    @is_admin()
    async def rr_add(self, interaction: discord.Interaction, message_id: str, emoji: str, role: discord.Role):
        config = load_config()
        if "reaction_roles" not in config:
            config["reaction_roles"] = {}

        msg_id = str(message_id)
        if msg_id not in config["reaction_roles"]:
            config["reaction_roles"][msg_id] = {}

        config["reaction_roles"][msg_id][str(emoji)] = role.id
        save_config(config)

        # Try to add the reaction
        try:
            msg = await interaction.channel.fetch_message(int(message_id))
            await msg.add_reaction(emoji)
        except:
            pass

        await interaction.response.send_message(f"Added {emoji} → {role.mention}", ephemeral=True)

    @app_commands.command(name="rr_remove", description="Remove reaction role")
    @is_admin()
    async def rr_remove(self, interaction: discord.Interaction, message_id: str, emoji: str):
        config = load_config()
        msg_id = str(message_id)

        if msg_id in config.get("reaction_roles", {}) and str(emoji) in config["reaction_roles"][msg_id]:
            del config["reaction_roles"][msg_id][str(emoji)]
            save_config(config)
            await interaction.response.send_message(f"Removed {emoji}", ephemeral=True)
        else:
            await interaction.response.send_message("Not found.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        config = load_config()
        data = config.get("reaction_roles", {}).get(str(payload.message_id))
        if not data:
            return

        emoji = str(payload.emoji)
        role_id = data.get(emoji)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id) if guild else None
        member = guild.get_member(payload.user_id) if guild else None

        if role and member:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        config = load_config()
        data = config.get("reaction_roles", {}).get(str(payload.message_id))
        if not data:
            return

        emoji = str(payload.emoji)
        role_id = data.get(emoji)
        if not role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(role_id) if guild else None
        member = guild.get_member(payload.user_id) if guild else None

        if role and member:
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
