import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="利用可能なコマンドとその説明を表示します")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(title="利用可能なコマンド", description="以下は利用可能なスラッシュコマンドの一覧です。", color=discord.Color.blue())

        # Get all global application commands
        commands_list = await self.bot.tree.fetch_commands()

        if not commands_list:
            embed.add_field(name="コマンドなし", value="現在、利用可能なコマンドはありません。", inline=False)
        else:
            for command in commands_list:
                embed.add_field(name=f"/{command.name}", value=command.description or "説明なし", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
