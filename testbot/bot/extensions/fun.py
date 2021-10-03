import lightbulb
import random
import hikari
import requests
from hikari.colors import Color

import datetime as dt

from testbot.bot import Bot



class Fun(lightbulb.Plugin):
    @lightbulb.command(name="dice", aliases=("roll",))
    async def command_dice(self, ctx: lightbulb.Context, dice: str) -> None:
        """Play a roll dice."""
        number, highest = (int(term) for term in dice.split("d"))

        if number > 25:
            return await ctx.respond("I can only roll up to 25 dice at one time.")


        rolls = [random.randint(1, highest) for i in range(number)]
        await ctx.respond(" + ".join(str(r) for r in rolls) + f" = {sum(rolls):,}", reply=True, mentions_reply=True)


    @lightbulb.command(name="say")
    async def command_say(self, ctx: lightbulb.Context, *, text: str) -> None:
        print(text)

        await ctx.respond(f"``{text}``")

    @lightbulb.command(name="cat", aliases=("gato",))
    async def command_cat(self, ctx: lightbulb.Context) -> None:
        image_url = requests.get("https://some-random-api.ml/img/cat")
        image_link = image_url.json()
        image = image_link['link']


        embed = (hikari.Embed(
            colour=Color(0x36393f),
            timestamp=dt.datetime.now().astimezone()
        )
        .set_footer(text=f"Requestest by {ctx.member.display_name}", icon=ctx.author.avatar_url)
        .set_image(image)
    )

        await ctx.respond(embed=embed, reply=True)


def load(bot: Bot) -> None:
    bot.add_plugin(Fun())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Fun")
