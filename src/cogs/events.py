import discord
from discord.ext import commands
from libs.message_handler import MessageHandler

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the message is a reply
        if message.reference and message.reference.resolved:
            replied_to_message = message.reference.resolved
            
            # Check if the replied-to message is from the bot and is a 'batou' message
            if replied_to_message.author == self.bot.user and \
               replied_to_message.content.endswith('♡') and \
               not replied_to_message.content.endswith('♡♡♡'):
                
                quoted_content = "\n".join([f"> {line}" for line in message.content.splitlines()])
                reply_content = MessageHandler.get('events.reply_to_batou', quoted_content=quoted_content)
                await message.reply(reply_content)

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))