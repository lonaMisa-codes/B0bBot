import discord
from discord import app_commands
from discord.ext import commands
import ast
import operator

# Safe math evaluator
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(node)
    return _eval(ast.parse(expr, mode='eval').body)

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="calc", description="Calculate a math expression")
    @app_commands.describe(expression="Math expression (e.g. 5*2000+100)")
    async def calc(self, interaction: discord.Interaction, expression: str):
        try:
            result = safe_eval(expression.replace(",", "").replace(" ", ""))
            embed = discord.Embed(title="Calculator", color=0x5865F2)
            embed.add_field(name="Expression", value=f"`{expression}`", inline=False)
            embed.add_field(name="Result", value=f"**{result:,}**", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message("Invalid expression.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Calculator(bot))
