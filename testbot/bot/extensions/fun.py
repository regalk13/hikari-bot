from math import trunc
from re import L
import lightbulb
import random
import hikari
import wikipedia
import requests
import asyncio
from hikari.colors import Color

import datetime as dt
from datetime import datetime, timedelta
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

@plugin.command
@lightbulb.set_help("Search in te PEP of python.")
@lightbulb.option("number", "The PEP number to search for.")
@lightbulb.command("pep", "Retrieve info on a Python Extension Protocol.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_pep(ctx: lightbulb.SlashContext) -> None:
    n = ctx.options.number
    url = f"https://python.org/dev/peps/pep-{n:>04}"

    async with ctx.bot.d.session.get(url) as r:
        if not r.ok:
            await ctx.respond(f"PEP {n:>04} could not be found")
            return

    await ctx.respond(f"PEP {n:>04}: <{url}>")

@plugin.command
@lightbulb.set_help("Search something using Google.")
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("google", "Let me Google that for you...")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_google(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://letmegooglethat.com/?q={q.replace(' ', '+')}>")


@plugin.command
@lightbulb.set_help("Search something using Duck Duck Go.")
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("duckduckgo", "Let me Duck Duck Go that for you...")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_duckduckgo(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://lmddgtfy.net/?q={q.replace(' ', '+')}>")

@plugin.command
@lightbulb.set_help("Give a cookie (1 hour cooldown).")
@lightbulb.add_cooldown(length=3600, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "User you want give the cookie", hikari.Member)
@lightbulb.command(name="givecookie", aliases=("gcookie",), description="Give a cookie to a user.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_cookie(ctx: lightbulb.SlashContext) -> None:

    target = ctx.options.user

    if target.id == ctx.member.id:
        await ctx.respond("You can't give a cookie to yourself.")
        return

    if target.is_bot:
        await ctx.respond("You can't give cookies to bots.")
        return

    await plugin.bot.d.db.execute(
         "UPDATE user SET cookies = cookies + 1 WHERE user_id = ?", 
          target.id
        )
   
    row = await ctx.bot.d.db.try_fetch_record(
        "SELECT cookies FROM user WHERE user_id = ?",
        target.id,
    )

    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    images_cookies = ["https://i.pinimg.com/originals/fc/39/65/fc3965c433c19f4492d616f975316c8c.gif", "https://64.media.tumblr.com/2f272878761f85dbe7665c1fada53e45/c0f2b8287c49f60d-4b/s540x810/aecab8278a4762d638af1a6dcda55e16c069c458.gif", "https://c.tenor.com/zEWVjcnOt1IAAAAC/anime-eating.gif", "https://c.tenor.com/bBRCCeAYPU8AAAAC/cookie-mashiro.gif"]

    embed = (hikari.Embed(
        description=f"You gave a cookie to **{target.username}**, now he/she has **{row.cookies}**",
        colour=Color.from_rgb(r_g, r_b, r_r)

    )
    .set_image(random.choice(images_cookies))
    )


    await ctx.respond(embed)

@plugin.command()
@lightbulb.set_help("Set a reminder, will be DM reminder or channel reminder.")
@lightbulb.option("reminder", "Reminder you want to set.")
@lightbulb.option("time", "Time to end the reminder.", default="5m")
@lightbulb.command(name="reminder", aliases=("remind",), description="Set a reminder")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_reminder(ctx: lightbulb.SlashContext) -> None:
    time = ctx.options.time
    reminder = ctx.options.reminder
    embed = (hikari.Embed(color=0xfa2617, timestamp=datetime.utcnow().astimezone()))
    embed_accepted = (hikari.Embed(color=0x5deb1f, timestamp=datetime.utcnow().astimezone()))

    #embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{ctx.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `/help reminder` for more information.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        embed_accepted.add_field(name="Reminder Set", value=f"Alright {ctx.member.username}, I will remind you about ``{reminder}`` in {counter}.")
        await ctx.respond(embed_accepted)
        await asyncio.sleep(seconds)
        await ctx.respond(f"Hi {ctx.member.mention}, you asked me to remind you about ``{reminder}`` {counter} ago.", user_mentions=True)
        return

    await ctx.respond(embed=embed)

@plugin.command
@lightbulb.set_help("Give answers to your questions")
@lightbulb.option("question", "The qeustion you want answers")
@lightbulb.command("8ball", description="Make the game of the 8ball")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_ball(ctx: lightbulb.SlashContext):
    
    responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]


    await ctx.respond(f"🎱 {random.choice(responses)}")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)