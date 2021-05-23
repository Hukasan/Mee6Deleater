from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Emoji,
)
from discord.ext.commands import Cog, Bot, Context
from discord.abc import GuildChannel, PrivateChannel
from apps.myembed import MyEmbed, scan_footer

# from datetime import datetime
# from pytz import utc
# from Cogs.app.MakeEmbed import MakeEmbed


class ReactionEvent(Cog, name="ReactionEvent"):
    """
    リアクションに対しての処理
    次に行う処理をbot.configにかんすうごと保存し、ここで呼び出す
    識別はembedのフッターを利用している(myembed.scan_footer)
    era:embed_reaction_action
    """

    qualified_name = "hide"

    def __init__(self, bot: Bot):
        self.bot = bot

    async def do_era(self, usr_id: int, ms: Message, react: str, arg: list) -> bool:
        usr = self.bot.get_user(usr_id)
        func = None
        if react == "🗑":
            if usr in ms.mentions:
                await ms.delete()
            return
        for count, d_b in enumerate(self.bot.down_bottoms):
            if d_b == react:
                buttoms_under = self.bot.bottom_under[str(ms.guild.id)].get(ms.id)[0]
                if buttoms_under:
                    await ms.clear_reactions()
                    for b in buttoms_under:
                        await ms.add_reaction(b)
                    await ms.add_reaction(self.bot.up_bottoms[count])
                    return
                else:
                    break
        for count, u_b in enumerate(self.bot.up_bottoms):
            if react == u_b:
                buttoms_upper = self.bot.bottom_upper[str(ms.guild.id)].get(ms.id)[0]

                if buttoms_upper:
                    await ms.clear_reactions()
                    await ms.add_reaction(self.bot.down_bottoms[count])
                    await ms.add_reaction("🗑")
                    for b in buttoms_upper:
                        await ms.add_reaction(b)
                    return
                else:
                    break
        if arg:
            func = self.bot.funcs.get(arg[0])
            if func:
                ctx = await self.bot.get_context(ms)
                return await func(self.bot, usr_id, ctx, react, arg[1:])

    @Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        emoji = str(rrae.emoji)

        if bool(channel) & bool(emoji) & bool(usr):
            if usr.bot:
                return
            ms = Message
            ms = await channel.fetch_message(id=rrae.message_id)
            if ms.embeds:
                for embed in ms.embeds:
                    await self.do_era(
                        usr_id=rrae.user_id,
                        ms=ms,
                        react=emoji,
                        arg=scan_footer(embed=embed),
                    )
            else:
                if emoji == "🗑":
                    for r in ms.reactions:
                        if (r.emoji == emoji) & (r.me):
                            if ms.author == usr:
                                await ms.delete()
                                return
                pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))
