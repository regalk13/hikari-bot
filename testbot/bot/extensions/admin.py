import lightbulb

from testbot.bot import Bot

class Admin(lightbulb.Plugin):
    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="shutdown", aliases=("sd",))
    async def command_shutdown(self, ctx: lightbulb.Context) -> None:
        """Shutdown the bot (Only app owner)."""
        await ctx.bot.close()


def load(bot: Bot) -> None:
    bot.add_plugin(Admin())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")