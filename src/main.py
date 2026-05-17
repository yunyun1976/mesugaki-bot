import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from libs import master_handler, db_handler, config_handler
from libs.constants import JST
from libs.message_handler import MessageHandler
import datetime
import random

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):

        # Add interaction check
        async def global_interaction_check(interaction: discord.Interaction) -> bool:
            # 1. 何よりも先に、まずdeferする (1msでも早くDiscordに応答を返す)
            if interaction.type == discord.InteractionType.application_command:
                if not interaction.response.is_done():
                    # 公開コマンドか判定
                    command_name = interaction.data.get('name') if interaction.data else None
                    is_public = command_name in ['batou', 'wakarase']
                    await interaction.response.defer(ephemeral=not is_public)

            # 2. その後、時間をかけて重い処理（JST取得、メッセージロード、判定など）を行う
            now = datetime.datetime.now(JST)
            if now.hour >= 21 or now.hour < 6:
                sleeping_messages = MessageHandler.get('sleeping.random_messages')
                await interaction.followup.send(random.choice(sleeping_messages), ephemeral=True)
                return False
            return True

        self.tree.interaction_check = global_interaction_check

        # Load cogs
        for filename in os.listdir('./src/cogs'):
            if filename.endswith('.py') and not filename.startswith('__') and filename != 'help.py':
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded cog: {filename}')
                except Exception as e:
                    print(f'Failed to load cog {filename}: {e}')
        # Load help cog last to ensure all commands are registered
        try:
            await self.load_extension('cogs.help')
            print('Loaded cog: help.py')
        except Exception as e:
            print(f'Failed to load cog help.py: {e}')
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        # Send startup message to all registered channels
        channels = config_handler.get_all_announcement_channels()
        for guild_id, channel_id in channels:
            channel = self.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(MessageHandler.get('system.startup', name=self.user.name))
                except Exception as e:
                    print(f"Failed to send startup message to {channel_id}: {e}")

bot = MyBot()


# Run the bot
if __name__ == "__main__":
    db_handler.init_db('barizougon.db')
    db_handler.init_db('abikyoukan.db')
    master_handler.init_masters_db()
    config_handler.init_config_db()
    if TOKEN is None:
        print("Error: DISCORD_TOKEN is not set in .env file.")
    else:
        bot.run(TOKEN)
