from __future__ import annotations

from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

import os
import hikari
import lightbulb
import logging

class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        self._extensions = [p.stem for p in Path(".").glob("./testbot/bot/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/token") as f:
            token = f.read().strip("\n")

        super().__init__(
            prefix="-",
            token=token,
            intents=hikari.Intents.ALL,
        ) 


    @staticmethod
    async def guild_only(message: hikari.Message) -> bool:
        return message.guild_id is not None


    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        
        super().run(
            activity=hikari.Activity(
                name=f"-help | Version 2.0", 
                type=hikari.ActivityType.WATCHING,
            ),
            status='idle'
        )

    async def close(self) -> None:
        await self.stdout_channel.send(f"Testing v is shutting now :(") 
        await super().close()

    async def on_starting(self, event: hikari.StartingEvent) -> None: 
        self.load_extensions_from("./testbot/bot/extensions/", must_exist=True)


    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        #self.add_check(self.guild_only)
        self.stdout_channel = await self.rest.fetch_channel(887515478304624730)
        #await self.stdout_channel.send(f"Testing v2.0 now online!") 
         
        logging.info("BOT READY!!!")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()
