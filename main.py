from file_io.file_io_s3 import json_io_s3 as jis

from os import environ, listdir, path
from discord.ext.commands import Bot
from discord import Intents, Guild, Role

from discord.ext.tasks import loop


p = "Cogs"
files = listdir(p)
extensions = [path.splitext(f)[0] for f in files if path.isfile(path.join(p, f))]

intents = Intents
intents = Intents.all()
intents.typing = False
intents.bans = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
intents.dm_messages = False
intents.dm_reactions = False

setup = jis("setup_test").iterate()
setupdict = setup.get()
servers = jis("servers_test").iterate()


if __name__ == "__main__":
    bot = Bot(
        command_prefix="?",
        description=setupdict["DESC"],
        intents=intents,
        case_insensitive=True,
    )
    bot.funcs = {}
    bot.ready_road_once_flag = False
    bot.loop_functions = []
    bot.ready_functions = []
    bot.up_bottoms = ["🔼"]
    bot.down_bottoms = ["⏬"]
    bot.bottom_upper = {}
    bot.bottom_under = {}
    bot.ms_author = {}
    bot.setup = setup.get()
    bot.setup_ite = setup
    bot.servers = servers.get()
    bot.servers_ite = servers
    bot.help_dict = {}

    async def loop_start():
        await loop_update.start()

    @loop(hours=3.0)
    async def loop_update():
        update_servers()
        pass

    def update_servers():
        db = servers.get()
        for g in bot.guilds:
            server = db.get(str(g.id))
            if bot.bottom_under.get(g.id):
                bot.bottom_under.update({str(g.id): {}})
                bot.bottom_upper.update({str(g.id): {}})
                bot.bottom_under_args.update({str(g.id): {}})
                bot.bottom_upper_args.update({str(g.id): {}})
            if server:
                if g.rules_channel:
                    server.update({"rules_channel": g.rules_channel.id})
            else:
                if g.rules_channel:
                    db.update({g.id: {"rules_channel": g.rules_channel.id}})
                else:
                    db.update({g.id: {"rules_channel": None}})
            for role in g.roles:
                if role.is_bot_managed and (role.name == bot.user.name):
                    db[str(g.id)].update({"bot_role": role.id})
        servers.put(db)
        bot.setup = setup.get()
        bot.servers = db

    bot.loop_functions.append(loop_start)

    @bot.listen()
    async def on_ready():
        if bot.ready_road_once_flag:
            return
        else:
            bot.ready_road_once_flag = True
        update_servers()
        if bot.loop_functions:
            for func in bot.loop_functions:
                await func()
        if bot.ready_functions:
            for func in bot.ready_functions:
                await func()

    bot.add_listener(on_ready)

    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(bot.setup["TOKEN"])
