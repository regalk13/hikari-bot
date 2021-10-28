from __future__ import annotations

import logging
import lightbulb
import wikipedia
import hikari
from lightbulb import plugins
from testbot.bot import Bot

class ErrorHandler(lightbulb.Plugin):
    @plugins.listener()
    async def on_command_error(self, event: lightbulb.CommandErrorEvent) -> None:

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

        if isinstance(event.exception, wikipedia.exceptions.DisambiguationError):
            return await event.context.respond("<a:Wrong:893873540846198844> try to be clearer with the search, multiple results found.")


        await event.context.respond("I have a error, please help me <:tiste:889343933304426536>")
        raise event.exception



def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())

def unload(bot: Bot) -> None:
    bot.remove_plugin("ErrorHandler")
