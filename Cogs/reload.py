from discord import Guild
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    command,
    is_owner,
    Group,
    Command,
    group,
)


class Developper(Cog):
    """
    開発者コマンド
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(aliases=["re", "lode", "l", "れ"], description="プログラムを再読み込み")
    async def load(self, ctx: Context):
        """
        プログラムを再読み込み。内部データは初期化される
        """
        for extension in list(self.bot.extensions):
            self.bot.reload_extension(f"{extension}")
            print(f"{extension}:is_reloted")
        print("再読み込み完了")
        await ctx.message.add_reaction("☑")


def setup(bot: Bot):
    return bot.add_cog(Developper(bot))
