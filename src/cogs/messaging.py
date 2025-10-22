import discord
from discord.ext import commands
from discord import app_commands
from libs import db_handler

class Messaging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _send_random_phrase_helper(self, interaction: discord.Interaction, db_name: str, suffix: str):
        phrase = db_handler.get_random_phrase(db_name)
        if phrase:
            await interaction.response.send_message(phrase + suffix)
        else:
            await interaction.response.send_message("ネタ切れです...", ephemeral=True)

    @app_commands.command(name="batou", description="罵倒します")
    async def batou(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, "barizougon.db", "♡")

    @app_commands.command(name="wakarase", description="わからせます")
    async def wakarase(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, "abikyoukan.db", "ぉぉぉお♡♡♡")

    async def _add_phrase_helper(self, interaction: discord.Interaction, phrase: str, db_name: str):
        if len(phrase) > 50:
            await interaction.response.send_message("フレーズは50文字以内で入力してください。", ephemeral=True)
            return

        if db_handler.add_phrase(db_name, phrase):
            await interaction.response.send_message(f"「{phrase}」を追加しました")
        else:
            await interaction.response.send_message(f"「{phrase}」は既に存在します", ephemeral=True)

    @app_commands.command(name="add_batou", description="罵倒の語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    async def add_batou(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, "barizougon.db")

    @app_commands.command(name="add_wakarase", description="わからせの語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    async def add_wakarase(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, "abikyoukan.db")


async def setup(bot: commands.Bot):
    await bot.add_cog(Messaging(bot))
