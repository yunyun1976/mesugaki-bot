import discord
from discord.ext import commands
from discord import app_commands
from libs import db_handler

class Messaging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            
            await interaction.response.send_message(f"どーてーは{error.retry_after:.2f}秒も待てないの?♡", ephemeral=True)
        else:
            raise error

    async def _send_random_phrase_helper(self, interaction: discord.Interaction, db_name: str, suffix: str):
        phrase = db_handler.get_random_phrase(db_name)
        if phrase:
            await interaction.response.send_message(phrase + suffix)
        else:
            await interaction.response.send_message("データベーススカスカじゃん♡ 早く言葉登録してよね♡", ephemeral=True)

    @app_commands.command(name="batou", description="罵倒します")
    async def batou(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, "barizougon.db", "♡")

    @app_commands.command(name="wakarase", description="わからせます")
    async def wakarase(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, "abikyoukan.db", "ぉぉぉお♡♡♡")

    async def _add_phrase_helper(self, interaction: discord.Interaction, phrase: str, db_name: str):
        if len(phrase) > 100:
            await interaction.response.send_message("なっが～♡ 100文字以内で我慢してよね♡", ephemeral=True)
            return

        if db_handler.add_phrase(db_name, phrase):
            await interaction.response.send_message(f"「{phrase}」ね♡ 新しい言葉、アタシが覚えててあげる♡")
        else:
            await interaction.response.send_message(f"「{phrase}」なんてもう知ってるし♡ ザコは同じことばっかり言うよね♡", ephemeral=True)

    @app_commands.command(name="add_batou", description="罵倒の語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: i.user.id)
    async def add_batou(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, "barizougon.db")

    @app_commands.command(name="add_wakarase", description="わからせの語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: i.user.id)
    async def add_wakarase(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, "abikyoukan.db")


async def setup(bot: commands.Bot):
    await bot.add_cog(Messaging(bot))
