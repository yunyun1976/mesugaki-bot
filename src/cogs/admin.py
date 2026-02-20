import discord
from discord.ext import commands
from discord import app_commands
from libs import db_handler, master_handler
from typing import List

# Helper View for pagination
class PaginationView(discord.ui.View):
    def __init__(self, phrases: List[str], title: str):
        super().__init__(timeout=60.0)
        self.phrases = phrases
        self.title = title
        self.current_page = 0
        self.per_page = 10
        self.total_pages = -(-len(self.phrases) // self.per_page)  # Ceiling division

    async def get_page_content(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_phrases = self.phrases[start:end]
        
        embed = discord.Embed(
            title=self.title,
            description="```\n" + "\n".join(page_phrases) + "\n```",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"ページ {self.current_page + 1}/{self.total_pages}")
        return embed

    async def update_buttons(self):
        # Disable previous button on first page
        self.children[0].disabled = self.current_page == 0
        # Disable next button on last page
        self.children[1].disabled = self.current_page >= self.total_pages - 1

    @discord.ui.button(label="前へ", style=discord.ButtonStyle.blurple)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        await self.update_buttons()
        embed = await self.get_page_content()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="次へ", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        await self.update_buttons()
        embed = await self.get_page_content()
        await interaction.response.edit_message(embed=embed, view=self)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_authorized(self, interaction: discord.Interaction) -> bool:
        """Checks if the user is an administrator or a master user."""
        return interaction.user.guild_permissions.administrator or master_handler.is_master(interaction.user.id)

    async def _get_phrases_paginated(self, interaction: discord.Interaction, db_name: str, title: str):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("キミには権限がないみたいだね♡管理者かマスターユーザーになってからもう一回おいで♡", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        phrases = db_handler.get_all_phrases(db_name)

        if not phrases:
            await interaction.followup.send("まだ何も登録されてないみたいだよ♡ ザコは早く登録しなよね♡")
            return

        view = PaginationView(phrases, title)
        await view.update_buttons()
        embed = await view.get_page_content()
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="get_barizougon", description="罵倒の語彙を全て取得します")
    async def get_barizougon(self, interaction: discord.Interaction):
        await self._get_phrases_paginated(interaction, "barizougon.db", "罵詈雑言一覧")

    @app_commands.command(name="get_abikyoukan", description="わからせの語彙を全て取得します")
    async def get_abikyoukan(self, interaction: discord.Interaction):
        await self._get_phrases_paginated(interaction, "abikyoukan.db", "阿鼻叫喚一覧")

    @app_commands.command(name="remove_batou", description="罵倒の語彙を削除します")
    @app_commands.describe(phrase="削除するフレーズ")
    async def remove_batou(self, interaction: discord.Interaction, phrase: str):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("キミには権限がないみたいだね♡管理者かマスターユーザーになってからもう一回おいで♡", ephemeral=True)
            return

        if db_handler.remove_phrase("barizougon.db", phrase):
            await interaction.response.send_message(f"「{phrase}」なんてザコな言葉、アタシが消してあげたよ♡感謝しなさいよね♡")
        else:
            await interaction.response.send_message(f"「{phrase}」なんて言葉、最初からなかったみたいだよ♡ キミの勘違いじゃない？♡", ephemeral=True)

    @app_commands.command(name="remove_wakarase", description="わからせの語彙を削除します")
    @app_commands.describe(phrase="削除するフレーズ")
    async def remove_wakarase(self, interaction: discord.Interaction, phrase: str):
        if not self.is_authorized(interaction):
            await interaction.response.send_message("キミには権限がないみたいだね♡管理者かマスターユーザーになってからもう一回おいで♡", ephemeral=True)
            return

        if db_handler.remove_phrase("abikyoukan.db", phrase):
            await interaction.response.send_message(f"「{phrase}」なんてザコな言葉、アタシが消してあげたよ♡感謝しなさいよね♡")
        else:
            await interaction.response.send_message(f"「{phrase}」なんて言葉、最初からなかったみたいだよ♡ キミの勘違いじゃない？♡", ephemeral=True)

    @app_commands.command(name="add_master", description="マスターユーザーを追加します")
    @app_commands.describe(user="追加するユーザー")
    async def add_master(self, interaction: discord.Interaction, user: discord.User):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("管理者さんだけが使えるんだよ〜♡ キミは使えないの、残念だったね♡", ephemeral=True)
            return

        if master_handler.add_master(user.id):
            await interaction.response.send_message(f"{user.mention} をマスターユーザーにしてあげたよ♡ アタシに感謝しなさいよね♡", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} はもうマスターユーザーだよ♡ 同じこと2回も言わせないでよね♡", ephemeral=True)

    @app_commands.command(name="check_master", description="マスターユーザーの一覧を表示します")
    async def check_master(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("管理者さんだけが使えるんだよ〜♡ キミは使えないの、残念だったね♡", ephemeral=True)
            return

        masters = master_handler.get_all_masters()
        if not masters:
            await interaction.response.send_message("マスターユーザーなんて一人もいないみたいだよ♡ ザコばっかりだね♡", ephemeral=True)
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
            await interaction.response.send_message("管理者さんだけが使えるんだよ〜♡ キミは使えないの、残念だったね♡", ephemeral=True)
            return

        if master_handler.remove_master(user.id):
            await interaction.response.send_message(f"{user.mention} をマスターユーザーから外してあげたよ♡ これでキミもただのザコだね♡", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} はもともとマスターユーザーじゃないみたいだよ♡ キミの勘違いじゃない？♡", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))