from discord import Guild
from discord.ext.tasks import loop
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
from apps.role_checker import check_role_is_upper_member as role_check


class Setting(Cog):
    """
    設定コマンド
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(description="消すまでの秒数を設定")
    async def time(self, ctx: Context, second):
        """
        消すまでの秒数を設定します
        Args:
            second (整数): [設定秒数]
        """
        second = int(second)
        serversdb = self.bot.servers_ite.get()
        if serversdb:
            self.bot.servers = serversdb
            temp = serversdb.get(str(ctx.guild.id))
            if temp:
                serversdb[str(ctx.guild.id)].update({"delay": second})
            else:
                serversdb.update({str(ctx.guild.id): {"delay": second}})
        else:
            serversdb = {str(ctx.guild.id): {"delay": second}}
        self.bot.server_ite.put(serversdb)
        return

    # @command()
    # async def togle(self,ctx:Context):


def setup(bot: Bot):
    return bot.add_cog(Setting(bot))
