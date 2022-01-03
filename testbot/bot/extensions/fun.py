from math import trunc
import lightbulb
import random
import hikari
import wikipedia
import requests
from hikari.colors import Color

import datetime as dt
from wikipedia import exceptions

from wikipedia.wikipedia import languages


plugin = lightbulb.Plugin(name="Fun", description="Fun commands for have fun with funny friends.")

@plugin.command()
@lightbulb.set_help("Make the dice roll, example of use: 2d5.")
@lightbulb.option("roll", "The numbers for make the roll.")
@lightbulb.command("dice", "Just make the dice roll, example: 2d5.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_dice(ctx: lightbulb.SlashContext) -> None:
    number, highest = (int(term) for term in ctx.options.roll.split("d"))

    if number > 25:
        return await ctx.respond("I can only roll up to 25 dice at one time.")


    rolls = [random.randint(1, highest) for i in range(number)]
    await ctx.respond(" + ".join(str(r) for r in rolls) + f" = {sum(rolls):,}", reply=True, mentions_reply=True)

@plugin.command()
@lightbulb.set_help("Search a cat image")
@lightbulb.command(name="cat", aliases=("gato",), description="Use to search a cat image.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_cat(ctx: lightbulb.SlashContext) -> None:
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

@plugin.command()
@lightbulb.set_help("Search wikipedia and receive in an embed")
@lightbulb.option("search", "Key word of the search you want")
@lightbulb.command(name="wikipedia", aliases=("wiki","wk"), description="Search a target in wikipedia.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_wikipedia(ctx: lightbulb.SlashContext) -> None:
    try:
        message = await ctx.respond("<a:Loading:893842133792997406> Searching...")
        page = wikipedia.page(ctx.options.search)
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
        .set_author(name=title,url=f"https://en.wikipedia.org/wiki/{title_link}")
        )

        await ctx.respond(embed, reply=True)
        await message.delete()

    except(wikipedia.exceptions.DisambiguationError):
        await message.edit(content="<a:Wrong:893873540846198844> try to be clearer with the search, multiple results found.")

    except(wikipedia.exceptions.PageError):
        await message.edit(content="<a:Wrong:893873540846198844> page not found.")

    except(wikipedia.exceptions.HTTPTimeoutError):
        await message.edit(content="<a:Wrong:893873540846198844> the servers seem to be down try again later.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)