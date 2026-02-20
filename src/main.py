import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from libs import master_handler, db_handler

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

bot = MyBot()


# Run the bot
if __name__ == "__main__":
    db_handler.init_db('barizougon.db')
    db_handler.init_db('abikyoukan.db')
    master_handler.init_masters_db()
    if TOKEN is None:
        print("Error: DISCORD_TOKEN is not set in .env file.")
    else:
        bot.run(TOKEN)
