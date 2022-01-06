from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from hikari.events.base_events import FailedEventT
import os
import hikari
import lightbulb
import logging

   
with open("./secrets/token") as f:
    token = f.read().strip("\n")

bot = lightbulb.BotApp(
        prefix="-",
        token=token,
        help_slash_command=True,
        default_enabled_guilds=(862093766646169609, 798708207668297749),
        case_insensitive_prefix_commands=True,
        intents=hikari.Intents.ALL,
) 

bot.load_extensions_from("./testbot/bot/extensions", must_exist=True)
bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None: 
    bot.d.scheduler.start()

@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    #self.add_check(self.guild_only)
    stdout_channel = await bot.rest.fetch_channel(887515478304624730)
    #await stdout_channel.send(f"Testing v2.0 now online!") 
         
    logging.info("BOT READY!!!")

@bot.listen(hikari.StoppingEvent)
async def on_stopping(event: hikari.StoppingEvent) -> None:
    bot.d.scheduler.shutdown() 
    #await bot.d.stdout_channel.send(f"Testing v is shutting now :(") 


@bot.listen(hikari.DMMessageCreateEvent)
async def on_dm_message_create(event: hikari.DMMessageCreateEvent) -> None:
    if event.message.author.is_bot:
        return

    await event.message.respond(
        f"The function of modmail is being carried out."
    )


@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[FailedEventT]) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return None

    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("<a:Warn:893874049967595550> Some arguments are missing: "+ ", ".join(event.exception.missing_args))


    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("<a:Warn:893874049967595550> Too many arguments were passed.")

    if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        return await event.context.respond(f"<a:Warn:893874049967595550> Command is on cooldown. Try again in {event.exception.retry_in:.0f} second(s).")

    if isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
        return await event.context.respond("<a:Wrong:893873540846198844> You don't have the required permissions for this action.")
        
    if isinstance(event.exception, lightbulb.errors.CheckFailure):
        return None

    await event.context.respond("An error has occurred <:tiste:889343933304426536>, it can be caused by the following:\n - The command is broken.\n - The command is under maintenance.\n - You don't use the command correctly look at its help.")
    raise event.exception


def run() -> None:
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name=f"/help • Version 2.0",
            type=hikari.ActivityType.WATCHING,
        )
    )