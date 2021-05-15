from discord import Message
from discord.ext import commands


class Message_Manage(commands.Cog):
    """
    会話干渉機能
    """

    qualified_name = "hide"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            if int(message.author.id) == (self.bot.setup.get().get("MEE6_ID")) and message.mentions:
                db = self.bot.db.get()
                serverdb = db.get(message.guild.id)
                if serverdb:
                    delay = serverdb.get("delay")
                    if delay and serverdb.get("swich"):
                        await message.delete(delay=delay)
                        return
                defdb = db.get("DEFAULT")
                if defdb:
                    if defdb.get("swith"):
                        await message.delete(delay=defdb.get("delay"))

        else:
            cont = message.content
            for prefix in self.bot.command_prefix:
                if "".join(cont[0 : len(prefix)]) == prefix:
                    await message.add_reaction("🗑")


def setup(bot):
    return bot.add_cog(Message_Manage(bot))
