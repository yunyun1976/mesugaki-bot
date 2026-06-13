import discord
from discord.ext import commands
from discord import app_commands

from libs import ng_word_handler
from libs.categories import Category
from libs.cog_utils import BaseCog, send_response
from libs.message_handler import MessageHandler

MAX_PHRASE_LENGTH = 100


class Messaging(BaseCog):
    @app_commands.command(name="batou", description="罵倒します")
    async def batou(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, Category.BATOU)

    @app_commands.command(name="wakarase", description="わからせます")
    async def wakarase(self, interaction: discord.Interaction):
        await self._send_random_phrase_helper(interaction, Category.WAKARASE)

    async def _send_random_phrase_helper(self, interaction: discord.Interaction, category: Category):
        phrase = await self.bot.phrase_repo.get_random(category)
        if phrase:
            await send_response(interaction, phrase + category.suffix)
        else:
            await send_response(interaction, MessageHandler.get('messaging.db_empty'), ephemeral=True)

    async def _add_phrase_helper(self, interaction: discord.Interaction, phrase: str, category: Category):
        if len(phrase) > MAX_PHRASE_LENGTH:
            await send_response(interaction, MessageHandler.get('messaging.add_too_long'), ephemeral=True)
            return

        if ng_word_handler.find_ng_match(phrase) is not None:
            await send_response(interaction, MessageHandler.get('messaging.add_ng_word'), ephemeral=True)
            return

        if await self.bot.phrase_repo.add(category, phrase):
            await send_response(interaction, MessageHandler.get('messaging.add_success', phrase=phrase))
        else:
            await send_response(interaction, MessageHandler.get('messaging.add_already_exists', phrase=phrase), ephemeral=True)

    @app_commands.command(name="add_batou", description="罵倒の語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: i.user.id)
    async def add_batou(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, Category.BATOU)

    @app_commands.command(name="add_wakarase", description="わからせの語彙を追加します")
    @app_commands.describe(phrase="追加するフレーズ")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: i.user.id)
    async def add_wakarase(self, interaction: discord.Interaction, phrase: str):
        await self._add_phrase_helper(interaction, phrase, Category.WAKARASE)


async def setup(bot: commands.Bot):
    await bot.add_cog(Messaging(bot))
