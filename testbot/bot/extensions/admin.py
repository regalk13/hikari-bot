import lightbulb


import typing as t
import logging


plugin = lightbulb.Plugin(name="Admin", description="Commands just the owner of the bot can use.")

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.set_help("Just the admin of the bot can shutdown the bot.")
@lightbulb.command(name="shutdown", aliases=("sd",), description="Shutdown the bot.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_shutdown(ctx: lightbulb.Context) -> None:
    await ctx.bot.close()

    
async def handle_extensions(ctx: lightbulb.Context, extensions: str, action: str) -> None:
    if extensions:
        extensions = extensions.split(" ")

    elif extensions == None:
        extensions = [e.split(".")[-1] for e in ctx.bot.extensions]

    count = 0
    for ext in extensions:
            try:
                getattr(ctx.bot, f"{action}_extensions")(f"testbot.bot.extensions.{ext.lower()}")
                logging.info(f"{ext} extension {action}ed.")
                count += 1

            except KeyError:
                logging.error(f"Extension {ext} could not be {action}ed.")

            except lightbulb.errors.ExtensionAlreadyLoaded:
                logging.error(f"Extension {ext} already {action}ed")


            except lightbulb.errors.ExtensionNotLoaded:
                logging.error(f"Extension {ext} is not loaded")


    await ctx.respond(f"<a:Right:893842032248885249> {count} extension(s) {action}ed.")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.set_help("Reload all extensions or add the name of just a extension.")
@lightbulb.option("extensions", "extensions you want to reload", required=False)
@lightbulb.command(name="reload", description="Reload the extensions")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_reload(ctx: lightbulb.Context) -> None:
    await handle_extensions(ctx, ctx.options.extensions, "reload")
        

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.set_help("Unload all extensions or add the name of just a extension.")
@lightbulb.option("extensions", "extensions you want to unload", required=False)
@lightbulb.command(name="unload", description="Unload the extensions")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_unload(ctx: lightbulb.Context) -> None:
    await handle_extensions(ctx, ctx.options.extensions, "unload")

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.set_help("Load the extensions or add the name of just a extension.")
@lightbulb.option("extensions", "extensions you want to load", required=False)
@lightbulb.command(name="load", description="Load the extensions")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_load(ctx: lightbulb.Context) -> None:
    await handle_extensions(ctx, ctx.options.extensions, "load")

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.set_help("Eval python code")
@lightbulb.option("query", "Query to run.")
@lightbulb.command(name="eval", description="Run python code.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_eval(ctx: lightbulb.SlashContext) -> None:
    result = eval(ctx.options.query)
    await ctx.respond(f"```py\n>>> {ctx.options.query}\n{result}```")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)