import lightbulb
import hikari
from testbot.bot import Bot


class Activity(lightbulb.Plugin):
    @lightbulb.command(name="youtube", aliases=("YT", "yt"))
    async def command_youtube(self, ctx: lightbulb.Context) -> None:
        """Give a greeting."""
        rest = hikari.api.RESTClient()
        invite = rest.create_invite()
        await ctx.respond(f"{invite}!", user_mentions=True)




def load(bot: Bot) -> None:
    bot.add_plugin(Activity())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Activity")