import discord
from discord import app_commands
from discord.ext import commands
import ast
import operator
import re

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def parse_number(text: str) -> float:
    """Supports k, m, b, t (case insensitive)"""
    text = text.lower().replace(",", "").strip()
    match = re.match(r'^([\d.]+)([kmbt])?$', text)
    if not match:
        return float(text)
    
    number, suffix = match.groups()
    number = float(number)
    
    multipliers = {
        'k': 1_000,          # thousand
        'm': 1_000_000,      # million
        'b': 1_000_000_000,  # billion
        't': 1_000_000_000_000  # trillion
    }
    
    if suffix in multipliers:
        return number * multipliers[suffix]
    return number

def safe_eval(expr: str):
    def replace_num(match):
        return str(parse_number(match.group(0)))
    
    expr = re.sub(r'[\d.]+[kmbtKMBT]?', replace_num, expr)
    expr = expr.replace(" ", "")

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
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

    @app_commands.command(name="calc", description="Calculate (supports k/m/b/t)")
    @app_commands.describe(expression="Example: 5*1.5m  or  2.5b/2  or  1t+500m")
    async def calc(self, interaction: discord.Interaction, expression: str):
        try:
            result = safe_eval(expression)
            embed = discord.Embed(title="Calculator", color=0x5865F2)
            embed.add_field(name="Expression", value=f"`{expression}`", inline=False)
            embed.add_field(name="Result", value=f"**{result:,.0f}**", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message("Invalid expression.\nExamples: `5*1.5m` `2b+300m` `1.2t`")

    @commands.command(name="calc")
    async def calc_prefix(self, ctx, *, expression: str):
        try:
            result = safe_eval(expression)
            embed = discord.Embed(title="Calculator", color=0x5865F2)
            embed.add_field(name="Expression", value=f"`{expression}`", inline=False)
            embed.add_field(name="Result", value=f"**{result:,.0f}**", inline=False)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Invalid expression.\nExamples: `5*1.5m` `2b+300m` `1.2t`")

async def setup(bot):
    await bot.add_cog(Calculator(bot))
