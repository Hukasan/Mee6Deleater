from discord import Emoji
from discord.ext.commands import Cog, Bot, HelpCommand, Group, Command, Context
import sys

from apps.myembed import MyEmbed
from file_io import file_io_s3 as fis
from apps.mymethods import lastone

EMBED_IDENTIFIER = "HELP_TABLE"
PAGE_DOWN_BOTTOM_COG = "💠"
PAGE_UP_BOTTOM = "🔼"


class Help(HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category_name = "Help"  # カテゴリが見つからなかった場合のカテゴリ
        self.command_attrs["description"] = "このメッセージを表示"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"
        self.command_attrs["aliases"] = ["he", "herupu", "へるぷ"]
        self.help_ite = fis.json_io_s3("help").iterate()
        self.help_dict = self.help_ite.get()
        self.dfembed = MyEmbed().clone()
        self.dfembed.change(
            help_mode=True,
            header="ℹBotInfo",
            header_icon=False,
            footer_arg=EMBED_IDENTIFIER,
            time=False,
            dust=True,
        )
        self.emojis = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

    async def create_category_tree(self, cmd, index=int(0), cmd_list=list()):
        """
        再帰関数。groupの最下層までを探索する
        """
        try:
            await cmd.can_run(self.context)
        except BaseException:
            print(f"例外:{cmd.name}")
            return ""
        content = str()
        temp = str()
        underber_p = int()
        name = str()
        params = ""
        if 0 >= index:
            pass
        else:
            underber_p = cmd.name.rfind("_")
            if index != 1:
                indent = (index) * "--"
            else:
                cmd_list.append(f"{cmd.full_parent_name} {cmd.name}")
                indent = f"**{len(cmd_list)}.**"
                # indent = f"**{count}.** "
                # count += 1
                if underber_p:
                    name = f"__{cmd.name[(underber_p + 1) :]}__"
                else:
                    name = f"__{cmd.name}__"
            params = " } { ".join(cmd.clean_params.keys())
            if params:
                params = "{ " + params + " }"
            content = f"{indent}{name}  {params}\r--{cmd.description}\n"
        if isinstance(cmd, Group):
            for subcmd in cmd.walk_commands():
                if not (subcmd.name == temp):
                    content_temp, cmd_list = await self.create_category_tree(
                        cmd=subcmd, index=(index + 1), cmd_list=cmd_list
                    )
                    content += content_temp
                temp = subcmd.name
            return content, cmd_list
        elif isinstance(cmd, Command):
            return content, cmd_list

    async def send_bot_help(self, mapping):
        content = str()
        count = 0
        cog_name_list = list()
        setup = self.context.bot.setup
        cog = Cog
        for cog in mapping:
            cog_name = cog.qualified_name if cog else self.no_category_name

            if (cog_name == "Help") | (cog_name == "hide"):
                continue
            content += f"**{self.emojis[count]}💠{cog_name}**\r"
            count += 1
            cog_name_list.append(cog.__class__.__name__)
        # opt = me.MyEmbed
        self.help_dict.update({"bot": cog_name_list})
        self.help_ite.put(self.help_dict)
        opt = self.dfembed.clone(self.context)
        opt.down_bottom = PAGE_DOWN_BOTTOM_COG
        opt.change(
            thumbnail=True,
            title=self.context.bot.user.name,
            description=str(
                f"⌘prifex=> **{str(self.context.bot.command_prefix[0])}** \n" f"{self.context.bot.description}\n"
            ),
            bottoms_under=self.emojis[:(count)],
            args_bottom_under=cog_name_list,
        )
        opt.add(
            name="> Command List",
            value=f"⌘**{self.context.prefix}help**\n--{self.command_attrs['description']}\n" f"{content}",
        )
        opt.add(name="> Invite click here⇓", value=f"{setup['INVITE']}")
        opt.add(
            name=f"> Suport click here⇓",
            value=str(f"{setup['SERVER']}\r" f"{setup['GITHUB']}"),
        )
        opt.footer_arg_add("bot")
        await opt.sendEmbed()

    async def send_cog_help(self, cog: Cog):
        # embed = me.MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        temp = str()
        command_name_list = list()
        count = 1
        empty_message = str()

        if cog.walk_commands:
            for cmd in cog.walk_commands():
                if (temp != cmd.name) & (not (cmd.root_parent)):
                    if self.help_dict.get(cog.qualified_name):
                        self.help_dict[cog.qualified_name].append(cmd.name)
                    else:
                        self.help_dict.update({cog.qualified_name: [cmd.name]})
                    self.help_ite.put(self.help_dict)
                    temp = cmd.name
                    embed.add(
                        name=f"> [{count}] {self.context.bot.command_prefix[0]}{cmd.name}",
                        value=f"{cmd.description}",
                    )
                    command_name_list.append(temp)
                    count += 1
        else:
            empty_message = "\rコマンドはありません"
        embed.change(
            header="💠Help",
            title=f"{cog.qualified_name}",
            description=f"{cog.description}{empty_message}",
            bottoms_under=self.emojis[: len(command_name_list)],
            args_bottom_under=command_name_list,
        )
        embed.footer_arg_add(cog.qualified_name)
        await embed.sendEmbed()

    async def send_group_help(self, group: Group):
        embed = MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        # value = "`" + "`, `".join(group.aliases) + "`"
        tab = "|"
        value = "以下の言葉でも呼び出し可能です"
        count = 0
        for a, lastone in lastone(group.aliases):
            if lastone:
                value += f"{tab}{a}```"
            elif count % 4 == 0:
                if count == 0:
                    value += f"```{a}"
                    count += 1
                else:
                    value += f"{tab}{a}\r"
            elif count % 4 == 1:
                value += a
            else:
                value += tab + a
            count += 1
        if group.help:
            embed.add(name="詳細", value="```" + group.help + "```", inline=False)
        content, cmd_name_list = await self.create_category_tree(group)
        embed.add(
            name="> subcommands",
            value=content,
            inline=True,
        )
        if group.aliases:
            embed.add(
                name="> Othercall",
                value=value,
                inline=True,
            )
        prefix = self.context.prefix if self.context.prefix else self.context.bot.command_prefix[0]
        self.help_dict[group.name] = cmd_name_list
        self.help_ite.put(self.help_dict)

        embed.change(
            header="⌘(親)Help",
            title=f"{prefix} {group.name} コマンド",
            description="__親cmdです、サブcmdが必要です__",
            bottoms_under=self.emojis[: len(cmd_name_list)],
            args_bottom_under=cmd_name_list,
        )
        embed.footer_arg_add
        await embed.sendEmbed(f"{group.name}")

    async def send_command_help(self, command: Command):
        params = " } { ".join(command.clean_params.keys())
        params = "{ " + params + " }"
        embed = MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        prefix = self.context.prefix if self.context.prefix else self.context.bot.command_prefix[0]
        embed.change(
            header="⌘Help",
            title=(f"**{prefix}{command.full_parent_name}__{(command.name).split('_')[-1]}__ {params}**"),
            description=f"```{command.help}```",
        )

        if command.aliases:
            # "`" + "`, `".join(command.aliases) + "`"
            value = "以下でも呼び出し可能(ローマ字は日本語でも可能)"
            count = 0
            tab = "|"
            for a, lastone in lastone(command.aliases):
                if lastone:
                    value += f"{tab}{a}```"
                elif count % 3 == 0:
                    if count == 0:
                        value += f"```{a}"
                        count += 1
                    else:
                        value += f"{tab}{a}\r"
                elif count % 3 == 1:
                    value += a
                else:
                    value += tab + a
                count += 1
            embed.add(
                name="> Othercall",
                value=value,
                inline=True,
            )

        embed.footer_arg_add(f"{command.name}")
        await embed.sendEmbed()

    async def send_error_message(self, error):
        embed = MyEmbed(self.context)
        embed.default_embed(header="ヘルプエラー", title="help対象が見つかりませんでした", description="入力を確認してもう一度お試しあれ")
        await embed.sendEmbed(greeting=f"{self.context.author.mention}")

    def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


async def era_h_table(bot: Bot, usr_id: int, ctx: Context, react: Emoji, footer_arg: list):
    help_dict = fis.json_io_s3("help").get()

    for index, emoji in enumerate(bot.help_command.emojis):
        if emoji == react:
            target = help_dict[footer_arg[0]][index]
            break

    if target == "bot":
        target = None
    print(target)
    await ctx.send_help(target)


def setup(bot: Bot):
    bot.help_command = Help()
    bot.funcs.update(
        {
            EMBED_IDENTIFIER: era_h_table,
        }
    )
    bot.up_bottoms.append(PAGE_UP_BOTTOM)
    bot.down_bottoms.append(PAGE_DOWN_BOTTOM_COG)
