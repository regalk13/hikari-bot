import lightbulb

from testbot.bot import Bot
class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        """Look at the latency of the bot."""
        await ctx.respond(f"Pong! Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")