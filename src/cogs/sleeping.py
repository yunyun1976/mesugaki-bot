import discord
from discord.ext import commands, tasks
from libs import config_handler
from libs.constants import JST
from libs.message_handler import MessageHandler
import datetime
import random

class Sleeping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduled_messages.start()

    def cog_unload(self):
        self.scheduled_messages.cancel()

    @tasks.loop(time=[datetime.time(hour=21, minute=0, tzinfo=JST),
                      datetime.time(hour=6, minute=0, tzinfo=JST)])
    async def scheduled_messages(self):
        now = datetime.datetime.now(JST)
        message = ""
        if now.hour == 21:
            message = MessageHandler.get('sleeping.good_night')
        elif now.hour == 6:
            message = MessageHandler.get('sleeping.wake_up')
        else:
            return

        channels = config_handler.get_all_announcement_channels()
        for guild_id, channel_id in channels:
            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(message)
                except discord.Forbidden:
                    print(f"Failed to send message to {channel_id}: Forbidden")
                except Exception as e:
                    print(f"Error in scheduled_messages: {e}")

    @scheduled_messages.before_loop
    async def before_scheduled_messages(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(Sleeping(bot))
