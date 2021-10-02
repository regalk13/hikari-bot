from __future__ import annotations

import logging
import lightbulb
import hikari
from lightbulb import plugins
from testbot.bot import Bot

class ErrorHandler(lightbulb.Plugin):
    @plugins.listener()
    async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:

        if isinstance(event.exception, lightbulb.errors.CommandNotFound):
            return None

        if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            return await event.context.respond("Some arguments are missing: "+ ", ".join(event.exception.missing_args))


        if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
            return await event.context.respond("Too many arguments were passed.")

        if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
            return await event.context.respond(f"Command is on cooldown. Truy again in {event.exception.retry_after:.0f} second(s).")

        if isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
            return await event.context.respond("You don't have the required permissions for this action.")
        

        await event.context.respond("I have a error, please help me <:tiste:889343933304426536>")
        raise event.exception



def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())

def unload(bot: Bot) -> None:
    bot.remove_plugin("ErrorHandler")