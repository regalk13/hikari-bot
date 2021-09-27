from __future__ import annotations

from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

import hikari
import lightbulb


class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self.extensions = [p.stem for p in Path(".").glob("./testbot/bot/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)


        super().__init__(
            prefix=">",
            insensitive_commands=True,
        ) 

    def setup(self) -> None:
        for ext in self.extensions:
            self.load_extension(f"test.bot.extensions.{ext}")
            logging.info(f"{ext} extension loaded")

    def rum(self) -> None:
        self.setup()

        with open("./secrets/token", mode="r", enconding="utf-8") as f:
            token = f.read()

        super().run(

        )