from discord import Embed, Message

from datetime import datetime
from Cogs.app.mymethods import dainyu
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
        self.bottoms = list()
        self.bottoms_sub = list()
        self.bottom_args = None
        self.image_url = dict()
        self.video = dict()

    def setTarget(self, target, bot=None):
        self.target = target
        if bot:
            self.bot = bot
        return self

    def change(
        self,
        time=True,
        mention=str(),
        mention_author=None,
        title=None,
        color=None,
        timestamp=str(),
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
        bottoms=list(),
        bottoms_sub=list(),
        bottom_args=None,
        image_url=None,
        video=None,
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
        self.bottoms = dainyu(bottoms, self.bottoms)
        self.bottoms_sub = dainyu(bottoms_sub, self.bottoms_sub)
        self.bottom_args = dainyu(bottom_args, self.bottom_args)
        self.time = dainyu(time, self.time)
        self.mention_author = dainyu(mention_author, self.mention_author)
        self.image_url = dainyu(image_url, self.image_url)
        self.video = dainyu(video, self.video)

    def setCtx(self, ctx):
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

    def default_embed(
        self,
        bot=None,
        time=True,
        mention=str(),
        mention_author=None,
        title=None,
        color=None,
        timestamp=str(),
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
        bottom_args=None,
        image_url=None,
        video=None,
    ) -> classmethod:
        """
        embed初期化
        Returns:
            このクラス
        """
        self.mention = mention
        self.mention_author = mention_author
        self.time = time
        self.title = title
        self.color = dainyu(color, self.color)
        self.footer = footer
        self.footer_icon = footer_icon
        self.header = header
        self.header_icon = header_icon
        self.thumbnai = thumbnail
        self.greeting = greeting
        self.footer_arg = footer_arg
        self.description = description
        self.dust = dust if (dust is not None) else self.dust
        self.bottom_args = bottom_args
        self.image_url = image_url
        self.video = video
        self.timestamp = timestamp
        return self

    def add(self, name: str, value: str, inline=False, greeting=str(), description=str()) -> None:
        if greeting:
            self.greeting = greeting
        self.description = description if description else self.description
        self.fields.append({"name": name, "value": value, "inline": inline})

    def clone(self, ctx=None) -> classmethod:

        return (copy(self)).setCtx(ctx)

    async def sendEmbed(
        self,
        obj=None,
        mention_author=None,
        mention=str(),
        greeting=str(),
        bottoms=list(),
        bottoms_sub=list(),
        bottom_args=None,
        dust=None,
    ) -> Message:
        """
        embed送信
        """
        self.mention = dainyu(mention, self.mention)
        self.mention_author = dainyu(mention_author, self.mention_author)
        self.greeting = dainyu(greeting, self.greeting)
        self.bottoms = dainyu(bottoms, self.bottoms)
        self.bottoms_sub = dainyu(bottoms_sub, self.bottoms_sub)
        self.bottom_args = dainyu(bottom_args, self.bottom_args)
        if self.mention:
            self.greeting = self.mention + self.greeting
        elif bool(self.mention_author) & bool(self.ctx):
            self.greeting = self.ctx.author.mention + self.greeting
        self.dust = dust if dust is not None else self.dust
        embed = await self.export_embed()
        obj = obj[0] if isinstance(self.obj, list) else self.obj
        if (not (self.obj)) & bool(self.target):
            obj = self.target
        elif self.ctx:
            obj = self.ctx.channel
        if obj:
            ms = await obj.send(embed=embed, content=self.greeting)
            if self.bottoms:
                for b in self.bottoms:
                    if b in UNICODE_EMOJI:
                        await ms.add_reaction(b)
            if self.bottoms_sub:
                await ms.add_reaction("🔽")
                self.bot.config[str(ms.guild.id)]["bottoms_sub"][ms.id] = self.bottoms_sub
                self.bot.config[str(ms.guild.id)]["bottoms"][ms.id] = self.bottoms
            if self.bottom_args:
                self.bot.config[str(ms.guild.id)]["bottom_args"][ms.id] = self.bottom_args
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
            config["footer"] = {"text": f"{self.footer}{'@' if self.footer_arg else ''}{self.footer_arg}"}
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
