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
from Cogs.app import table, make_embed as me, role_checker as ac, mymethods as mm


class Setting(Cog):
    """
    開発者コマンド
    """

    qualified_name = "hide"

    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(aliases=["re", "lode", "l", "れ"], description="プログラムを再読み込み")
    async def load(self, ctx: Context):
        for extension in list(self.bot.extensions):
            self.bot.reload_extension(f"{extension}")
            print(f"{extension}:is_reloted")
        print("再読み込み完了")
        await ctx.message.add_reaction("☑")


def setup(bot: Bot):
    return bot.add_cog(Setting(bot))
