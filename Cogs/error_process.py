from discord import Emoji, Message
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    command,
    is_owner,
    Group,
    Command,
)
from apps.myembed import MyEmbed
from apps.inputassist import hyokiyure

EMBED_IDENTIFIER = "ERROR_CMD_HELP"
E_CH_REACTION_ACCEPT = "🙆"


async def era_e_ch(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    if str(react) == E_CH_REACTION_ACCEPT:
        target = arg[1]
        await ctx.send_help(target)
        await ctx.message.delete()
    else:
        pass


class OutputError(Cog):
    qualified_name = "hide"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.owner = None
        self.__error_title = "コマンド実行時エラー"
        self.__error_fotter = "BotError"
        self._database_error = "データ変更にエラーがおきました\r今実行した処理は行なえませんでした。"
        self.__undefine_error_title = "想定外のエラー"
        self.__notice_owner_message_base = "ボット主に通達します.."
        self.__notice_owner_message = self.__notice_owner_message_base
        self.__missing_arg_message = "そのコマンドに必要な要素指定が足りていません\r" "コマンドの詳細を表示しますか？"
        self.__permission_message = "😢指定されたコマンドを実行する権限が貴方にありません\r必要があれば、管理者まで問い合わせください"

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        self.owner = self.bot.get_user(self.bot.owner_id)
        if self.owner:
            self.__notice_owner_message = self.owner.mention + self.__notice_owner_message_base
        cmd = str()
        embed = MyEmbed(ctx)
        try:
            dubleq = str(error).split('"')
            embed.default_embed(footer=self.__error_fotter, title=self.__error_title)
            if dubleq:
                if dubleq[0] == "Command " and dubleq[2] == " is not found":
                    flag = True
                    slist = hyokiyure(ctx.invoked_with, self.bot.all_commands.keys())
                    for cmd in slist:
                        if cmd:
                            if isinstance(cmd, list):
                                cmd = cmd[0]
                            temp = ctx.message
                            temp.content = self.bot.command_prefix[0] + cmd
                            await self.bot.process_commands(temp)
                            flag = False
                            break
                    if flag:
                        await ctx.message.add_reaction("❔")
                    return
                else:
                    embed.add(
                        name=self.__undefine_error_title,
                        value=f"```{str(error)}```",
                        greeting=self.__notice_owner_message,
                    )
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                    greeting=self.__notice_owner_message,
                )
        except IndexError:
            embed.default_embed(
                footer=self.__error_fotter,
                title=self.__error_title,
                greeting=f"{ctx.author.mention}",
                time=False,
            )
            if "required argument that is missing." in str(error):
                string = f"{ctx.command}"
                # if ctx.invoked_subcommand:
                #     string = (ctx.invoked_subcommand).name
                # else:
                #     string = f"{ctx.command}"
                embed.change(
                    description=self.__missing_arg_message,
                    footer_arg=f"{EMBED_IDENTIFIER} {string}",
                    bottoms=[E_CH_REACTION_ACCEPT],
                )
            elif "You do not own this bot." in str(error):
                embed.change_description(self.__permission_message)
            elif "The check functions for command cmd failed." in str(error):
                embed.change_description(self.__permission_message)
            elif "大変だデータベースエラー!":
                embed.change_description(self._database_error)
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                    greeting=self.__notice_owner_message,
                )
        await embed.sendEmbed()


def setup(bot):
    return
    # bot.config["funcs"].update(
    #     {
    #         EMBED_IDENTIFIER: era_e_ch,
    #     }
    # )
    # return bot.add_cog(OutputError(bot))
