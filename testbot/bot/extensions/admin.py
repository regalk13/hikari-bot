from __future__ import annotations


import lightbulb

from testbot.bot import Bot

import typing as t
import logging
class Admin(lightbulb.Plugin):
    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="shutdown", aliases=("sd",))
    async def command_shutdown(self, ctx: lightbulb.Context) -> None:
        """Shutdown the bot (Only app owner)."""
        await ctx.bot.close()

    
    async def handle_extensions(self, ctx: lightbulb.Context, extensions: str, action: str) -> None:
        if extensions:
            extensions = extensions.split(" ")

        else:
            extensions = [e.split(".")[-1] for e in ctx.bot.extensions]


        count = 0
        for ext in extensions:
            try:
                getattr(ctx.bot, f"{action}_extension")(f"testbot.bot.extensions.{ext.lower()}")
                logging.info(f"{ext} extension {action}ed.")
                count += 1

            except KeyError:
                logging.error(f"Extension {ext} could not be {action}ed.")

            except lightbulb.errors.ExtensionAlreadyLoaded:
                logging.error(f"Extension {ext} already {action}ed")


            except lightbulb.errors.ExtensionNotLoaded:
                logging.error(f"Extension {ext} is not loaded")


        await ctx.respond(f"{count} extension(s) {action}ed.")



    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="reload")
    async def command_reload(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        """Reload all extensions or only one (Only app owner)."""
        await self.handle_extensions(ctx, extensions, "reload")
        
    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="unload")
    async def command_unload(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        """Unload all extensions or only one (Only app owner)."""
        await self.handle_extensions(ctx, extensions, "unload")


    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="load")
    async def command_load(self, ctx: lightbulb.Context, *, extensions: str = "") -> None:
        """Unload all extensions or only one (Only app owner)."""
        await self.handle_extensions(ctx, extensions, "load")



def load(bot: Bot) -> None:
    bot.add_plugin(Admin())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")