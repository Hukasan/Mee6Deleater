from discord import Embed, Message

from datetime import datetime
from apps.mymethods import dainyu
from copy import copy
from emoji import UNICODE_EMOJI

"""
    embed作成、送信
"""


class MyEmbed:
    """
    embed作成、送信
    """

    def __init__(self, ctx=None):

        self.ctx = ctx
        self.bot = ctx.bot if ctx else None
        self.target = ctx.channel if ctx else None
        self.obj = None
        self.mention = str()
        self.mention_author = False
        self.help_mode = False
        self.title = str()  # タイトル
        self.color = 0x00FF00  # 色
        self.thumbnail = False  # 大きめのアイコン画像を表示させるかどうか
        self.footer = str()  # フッター文
        self.footer_icon = str()  # フッター画像url
        self.header = None  # ヘッダー文
        self.header_icon = str()  # ヘッダー画像url
        self.fields = list()
        self.description = str()
        self.descriptions = list()
        self.line_number = int(0)
        self.greeting = str()
        self.time = False
        self.dust = True
        self.footer_arg = str()
        self.bottoms_upper = (list(),)
        self.bottoms_under = (list(),)
        self.args_bottom_under = (list(),)
        self.args_bottom_upper = (list(),)
        self.image_url = dict()
        self.video = dict()

    def setTarget(self, target, bot=None):
        self.target = target
        if bot:
            self.bot = bot
        return self

    def change(
        self,
        time=None,
        mention=str(),
        mention_author=None,
        title=None,
        color=None,
        url=str(),
        description=None,
        thumbnail=False,
        header=str(),
        header_icon=None,
        footer=str(),
        footer_icon=str(),
        greeting=str(),
        footer_arg=str(),
        dust=None,
        bottoms_upper=list(),
        bottoms_under=list(),
        args_bottom_under=None,
        args_bottom_upper=None,
        image_url=None,
        video=None,
        help_mode=None,
    ):
        """
        設定書き換え
        """
        self.color = dainyu(color, self.color)
        self.thumbnail = dainyu(thumbnail, self.thumbnail)
        self.header = dainyu(header, self.header)
        self.header_icon = dainyu(header_icon, self.header_icon)
        self.footer = dainyu(footer, self.footer)
        self.title = dainyu(title, self.title)
        self.greeting = dainyu(greeting, self.greeting)
        self.description = dainyu(description, self.description)
        self.footer_arg = dainyu(footer_arg, self.footer_arg)
        self.bottoms_under = dainyu(bottoms_under, self.bottoms_under)
        self.bottoms_upper = dainyu(bottoms_upper, self.bottoms_upper)
        self.args_bottom_under = dainyu(args_bottom_under, self.args_bottom_under)
        self.args_bottom_upper = dainyu(args_bottom_upper, self.args_bottom_upper)
        self.time = dainyu(time, self.time)
        self.mention_author = dainyu(mention_author, self.mention_author)
        self.image_url = dainyu(image_url, self.image_url)
        self.video = dainyu(video, self.video)
        self.dust = dainyu(dust, self.dust)
        self.help_mode = dainyu(help_mode, self.help_mode)

    def setCtx(self, ctx):
        if ctx:
            self.ctx = dainyu(ctx, self.ctx)
            self.bot = dainyu(ctx.bot, self.bot)
        return self

    def setBot(self, bot):
        self.bot = bot
        return self

    def __cut(self, obj: str):
        point = 50
        if isinstance(obj, str):
            if len(obj) > point:
                ex = f"{obj[:point+1]}\n"
                ex = ex + (self.__cut(obj[point + 1 :]))
            else:
                ex = f"{obj}\n"
        else:
            ex = "TextError"
        return ex

    def __export_complist(self, obj):
        ex = list()
        lines = 0
        if isinstance(obj, str):
            obj = obj.splitlines()
        if isinstance(obj, list):
            temp = list()
            for o in obj:
                temp.extend(o.splitlines())
            obj = temp
            for o in obj:
                content = self.__cut(o)
                line = len(content)
                # print(f"{o},{line}")
                while line > 0:
                    if (line + lines) > 10:
                        if ex:
                            ex[-1] = ex[-1] + content[: 15 - lines + 1]
                        else:
                            ex.append(content[: 15 - lines + 1])
                        content = content[15 - lines + 1 :]
                        lines = 0
                        line = line - 15 + lines - 1
                    else:
                        if ex:
                            ex[-1] = ex[-1] + content
                        else:
                            ex.append(content)
                        line = 0
        return ex

    def default_embed(self) -> classmethod:
        """
        embed初期化
        Returns:
            このクラス
        """
        return self

    def add(self, name: str, value: str, inline=False, greeting=str(), description=str()) -> None:
        if greeting:
            self.greeting = greeting
        self.description = description if description else self.description
        self.fields.append({"name": name, "value": value, "inline": inline})

    def clone(self, ctx=None) -> classmethod:

        return (copy(self)).setCtx(ctx)

    def footer_arg_add(self, value: str):
        if self.footer_arg:
            self.footer_arg = self.footer_arg + " " + value
        else:
            self.footer_arg = value

    async def sendEmbed(self, obj=None) -> Message:
        """
        embed送信
        """
        if self.mention:
            self.greeting = self.mention + self.greeting
        elif bool(self.mention_author) & bool(self.ctx):
            self.greeting = self.ctx.author.mention + self.greeting
        elif bool(self.help_mode) & bool(self.ctx):
            if self.ctx.author.id == self.bot.user.id:
                user = self.ctx.message.mentions[0]
                if user:
                    self.greeting = user.mention + self.greeting
            else:
                self.greeting = self.ctx.author.mention + self.greeting
        embed = await self.export_embed()
        obj = obj[0] if isinstance(self.obj, list) else self.obj
        if (not (self.obj)) & bool(self.target):
            obj = self.target
        elif self.ctx:
            obj = self.ctx.channel
        if obj:
            ms = await obj.send(embed=embed, content=self.greeting)
            if self.bottoms_under:
                if self.bot.bottom_under.get(str(ms.guild.id)):
                    self.bot.bottom_under[str(ms.guild.id)].update(
                        {ms.id: [self.bottoms_under, self.args_bottom_under]}
                    )
                else:
                    self.bot.bottom_under.update(
                        {str(ms.guild.id): {ms.id: [self.bottoms_under, self.args_bottom_under]}}
                    )
            if self.bottoms_upper:
                for b in self.bottoms_upper:
                    if b in UNICODE_EMOJI:
                        await ms.add_reaction(b)
                if self.bot.bottom_upper.get(str(ms.guild.id)):
                    self.bot.bottom_upper[str(ms.guild.id)].update(
                        {ms.id: [self.bottoms_upper, self.args_bottom_upper]}
                    )
                else:
                    self.bot.bottom_upper.update(
                        {str(ms.guild.id): {ms.id: [self.bottoms_upper, self.args_bottom_upper]}}
                    )
            if self.dust:
                await ms.add_reaction("🗑")
        return ms

    async def export_embed(self) -> Embed:
        """
        embed生成

        Returns:
            Embed: 生成したembed
        """

        config = dict()
        config["color"] = self.color
        config["title"] = dainyu(self.title)
        config["description"] = dainyu(self.description)
        config["fields"] = self.fields
        config["video"] = self.video

        bot_info = await self.bot.application_info()

        if self.time:
            if isinstance(self.time, bool):
                config["timestamp"] = (
                    ((self.ctx.message.created_at).isoformat()) if self.ctx else ((datetime.utcnow()).isoformat())
                )
            else:
                config["timestamp"] = self.time.isoformat()
        if (bool(self.footer)) or (bool(self.footer_arg)):
            config["footer"] = {"text": f"{self.footer}{'@'+self.footer_arg if self.footer_arg else ''}"}
            if isinstance(self.footer_icon, str):
                config["footer"]["icon_url"] = str(self.footer_icon)
            elif bool(bot_info) & (isinstance(self.footer_icon, bool)) & bool(self.footer_icon):
                config["footer"]["icon_url"] = str(bot_info.icon_url)

        if ((bool(self.bot)) & self.thumbnail) & (bool(bot_info)):
            config["thumbnail"] = {"url": str(bot_info.icon_url)}

        if self.header:
            config["author"] = {"name": self.header}
            if isinstance(self.header_icon, str):
                config["author"]["icon_url"] = str(self.header_icon)
            elif bool(bot_info) & (isinstance(self.header_icon, bool)) & bool(self.header_icon):
                config["author"]["icon_url"] = str(bot_info.icon_url)
        if self.image_url:
            config["image"] = {"url": str(self.image_url)}

        return Embed.from_dict(config)

    def import_embed(self, embed: Embed):
        gotten_dict = embed.to_dict()
        (footer, footer_icon) = (
            (gotten_dict["footer"].get("text"), gotten_dict["footer"].get("icon_url"))
            if gotten_dict.get("footer")
            else (
                None,
                None,
            )
        )
        self.change(
            title=gotten_dict.get("title"),
            description=gotten_dict.get("description"),
            url=gotten_dict.get("url"),
            time=gotten_dict.get("timestamp"),
            footer=footer,
            footer_icon=footer_icon,
            color=gotten_dict.get("color"),
            thumbnail=gotten_dict.get("thumbnail"),
            image_url=gotten_dict.get("image").get("url") if gotten_dict.get("image") else None,
            video=gotten_dict.get("video"),
        )


def scan_footer(embed: Embed) -> list:
    footer = str()
    arg = list()
    if embed:
        footer = (embed.to_dict()).get("footer")
        if footer:
            text = footer.get("text")
            if "@" in text:
                arg = text.split("@")[-1]
                # print(arg.split(" "))
                return arg.split(" ")
    return list()
