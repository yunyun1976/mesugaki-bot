import discord
from discord.ext import commands
from discord import app_commands
from libs import db_handler, master_handler

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_authorized(self, interaction: discord.Interaction) -> bool:
        """Checks if the user is an administrator or a master user."""
        return interaction.user.guild_permissions.administrator or master_handler.is_master(interaction.user.id)

    @app_commands.command(name="get_barizougon", description="罵倒の語彙を全て取得します")
    async def get_barizougon(self, interaction: discord.Interaction):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("管理者またはマスターユーザーである必要があります。", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        phrases = db_handler.get_all_phrases("barizougon.db")
        if phrases:
            await interaction.followup.send("```\n" + "\n".join(phrases) + "\n```")
        else:
            await interaction.followup.send("まだ何も登録されていません")

    @app_commands.command(name="get_abikyoukan", description="わからせの語彙を全て取得します")
    async def get_abikyoukan(self, interaction: discord.Interaction):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("管理者またはマスターユーザーである必要があります。", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        phrases = db_handler.get_all_phrases("abikyoukan.db")
        if phrases:
            await interaction.followup.send("```\n" + "\n".join(phrases) + "\n```")
        else:
            await interaction.followup.send("まだ何も登録されていません")

    @app_commands.command(name="remove_batou", description="罵倒の語彙を削除します")
    @app_commands.describe(phrase="削除するフレーズ")
    async def remove_batou(self, interaction: discord.Interaction, phrase: str):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("管理者またはマスターユーザーである必要があります。", ephemeral=True)
            return

        if db_handler.remove_phrase("barizougon.db", phrase):
            await interaction.response.send_message(f"「{phrase}」を削除しました")
        else:
            await interaction.response.send_message(f"「{phrase}」は存在しません", ephemeral=True)

    @app_commands.command(name="remove_wakarase", description="わからせの語彙を削除します")
    @app_commands.describe(phrase="削除するフレーズ")
    async def remove_wakarase(self, interaction: discord.Interaction, phrase: str):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("管理者またはマスターユーザーである必要があります。", ephemeral=True)
            return

        if db_handler.remove_phrase("abikyoukan.db", phrase):
            await interaction.response.send_message(f"「{phrase}」を削除しました")
        else:
            await interaction.response.send_message(f"「{phrase}」は存在しません", ephemeral=True)

    @app_commands.command(name="add_master", description="マスターユーザーを追加します")
    @app_commands.describe(user="追加するユーザー")
    async def add_master(self, interaction: discord.Interaction, user: discord.User):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("管理者権限が必要です。", ephemeral=True)
            return

        if master_handler.add_master(user.id):
            await interaction.response.send_message(f"{user.mention} をマスターユーザーに追加しました。", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} は既にマスターユーザーです。", ephemeral=True)

    @app_commands.command(name="check_master", description="マスターユーザーの一覧を表示します")
    async def check_master(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("管理者権限が必要です。", ephemeral=True)
            return

        masters = master_handler.get_all_masters()
        if not masters:
            await interaction.response.send_message("マスターユーザーは登録されていません。", ephemeral=True)
            return

        embed = discord.Embed(title="マスターユーザー一覧")
        for user_id in masters:
            user = self.bot.get_user(user_id)
            embed.add_field(name=user.name if user else f"ID: {user_id}", value="", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="remove_master", description="マスターユーザーを削除します")
    @app_commands.describe(user="削除するユーザー")
    async def remove_master(self, interaction: discord.Interaction, user: discord.User):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("管理者権限が必要です。", ephemeral=True)
            return

        if master_handler.remove_master(user.id):
            await interaction.response.send_message(f"{user.mention} をマスターユーザーから削除しました。", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} はマスターユーザーではありません。", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))