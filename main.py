from file_io.file_io_s3 import json_io_s3 as jis

from os import environ, listdir, path
from discord.ext.commands import Bot
from discord import Intents


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

setup = jis("setup").get()

if __name__ == "__main__":
    bot = Bot(
        command_prefix=["?", "？"],
        description=setup["DESCRIPTION"],
        intents=intents,
        case_insensitive=True,
    )
    bot.config = {
        "funcs": {},
        "ready_is_road_once_flag": False,
        "loop_functions": [],
        "ready_functions": [],
    }

    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(setup["TOKEN"])
