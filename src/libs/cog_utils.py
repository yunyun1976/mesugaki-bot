import discord
from discord.ext import commands
from discord import app_commands

from libs import master_handler
from libs.message_handler import MessageHandler


async def send_response(
    interaction: discord.Interaction,
    content: str = None,
    *,
    embed: discord.Embed = None,
    view: discord.ui.View = None,
    ephemeral: bool = False,
) -> None:
    """interactionの状態に応じて response / followup を使い分けて送信する。

    グローバルなinteraction_checkで既にdeferされている場合は followup を、
    まだ応答していない場合は response.send_message を使用する。
    """
    kwargs = {"ephemeral": ephemeral}
    if content is not None:
        kwargs["content"] = content
    if embed is not None:
        kwargs["embed"] = embed
    if view is not None:
        kwargs["view"] = view

    if interaction.response.is_done():
        await interaction.followup.send(**kwargs)
    else:
        await interaction.response.send_message(**kwargs)


def is_authorized(interaction: discord.Interaction) -> bool:
    """ユーザーが管理者またはマスターユーザーかどうかを判定する。"""
    return interaction.user.guild_permissions.administrator or master_handler.is_master(interaction.user.id)


async def check_authorized(interaction: discord.Interaction) -> bool:
    """権限チェックを行い、権限がない場合はメッセージを送信してFalseを返す。"""
    if not is_authorized(interaction):
        await send_response(interaction, MessageHandler.get('common.no_permission'), ephemeral=True)
        return False
    return True


async def check_admin(interaction: discord.Interaction) -> bool:
    """管理者チェックを行い、管理者でない場合はメッセージを送信してFalseを返す。"""
    if not interaction.user.guild_permissions.administrator:
        await send_response(interaction, MessageHandler.get('common.admin_only'), ephemeral=True)
        return False
    return True


class BaseCog(commands.Cog):
    """共通のエラーハンドリングを提供するCog基底クラス。"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            content = MessageHandler.get('common.cooldown', retry_after=error.retry_after)
            await send_response(interaction, content, ephemeral=True)
        else:
            raise error
