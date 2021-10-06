import lightbulb
import random
import hikari
from lightbulb.converters import emoji_converter
import wikipedia
import requests
from hikari.colors import Color

import datetime as dt
from wikipedia import exceptions

from wikipedia.wikipedia import languages

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
        
        await ctx.message.delete()
        await ctx.respond(f"{text}")

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

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="wikilang", aliases=("wl",))
    async def command_wikilang(self, ctx:lightbulb.Context, language) -> None:
        global languages_
        languages_ = language

        await ctx.respond(f"<a:Right:893842032248885249> **{languages_}** language successfully changed")

    @lightbulb.command(name="wikipedia", aliases=("wiki","wk"))
    async def command_wikipedia(self, ctx: lightbulb.Context, *, search) -> None:
        try:
            message = await ctx.respond("<a:Loading:893842133792997406> Searching...")
            wikipedia.set_lang(languages_)
            page = wikipedia.page(search)
            image = page.images[0]
            title = page.title
            content = page.content
            if len(content) > 600:
                content = content[:600] + "...(READ MORE click on the title)"

            else:
                content = content

            title_link = title.replace(" ", "_")
            embed = (hikari.Embed(
                colour=Color(0x36393f),
                description=content,
                timestamp=dt.datetime.now().astimezone()

            )
            .set_image(image)
            .set_author(name=title,url=f"https://{languages_}.wikipedia.org/wiki/{title_link}")
            )

            await ctx.respond(embed)
            await message.delete()

        except(wikipedia.exceptions.DisambiguationError):
            await message.edit(content="<a:Wrong:893873540846198844> try to be clearer with the search, multiple results found.")

        except(wikipedia.exceptions.PageError):
            await message.edit(content="<a:Wrong:893873540846198844> page not found.")

        except(wikipedia.exceptions.HTTPTimeoutError):
            await message.edit(content="<a:Wrong:893873540846198844> the servers seem to be down try again later.")


def load(bot: Bot) -> None:
    bot.add_plugin(Fun())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Fun")
