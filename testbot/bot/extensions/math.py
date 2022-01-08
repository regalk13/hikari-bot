from typing import Type
from lightbulb import decorators
from lightbulb.utils.search import get
import wolframalpha
import lightbulb
import hikari
import json, asyncio, wolfram
from hikari.colors import Color
import urllib
import requests
import ast
plugin = lightbulb.Plugin(name="Math", description="Lows and advanced maths commands.")

with open("./secrets/api-math", "r") as f:
    app_id = f.readline()


# Search on wolfram website your api-key
app = wolfram.App(app_id)
   
@plugin.command
@lightbulb.set_help("Get the stats from wolframalpha")
@lightbulb.option("search", "The seacrh you need")
@lightbulb.command(name="w", aliases=("wolframalpha",), description="Seacrh something in wolframalpha")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_w(ctx: lightbulb.SlashContext) -> None:

    try:
        message = await ctx.respond("<a:Loading:893842133792997406> loading data...")
        data = app.full(ctx.options.search)
        data_ = data['queryresult']['pods']
        image = None
        title = data_[0]['subpods'][0]['img']['title']

        try:
            pods_content = data_[1]
            sub_pods_content = pods_content['subpods']
            image_content = sub_pods_content[0]['img']['src']
            image = image_content

        except KeyError:
            #print(data_)
            pods_title = data_[0]
            #print(pods_title)
            sub_pods_title = pods_title['subpods']
            #print(sub_pods)
            image_title = sub_pods_title[0]['img']['src']
            image = image_title

        embed = (hikari.Embed(
            title=f"**{title}**",
            color=Color(0x36393f),
        )
        .set_image(image)
        .set_footer(text=f"Requestest by {ctx.member.username}#{ctx.member.discriminator}", icon=ctx.member.avatar_url)
        )    

        await message.delete()
        await ctx.respond(embed)

    except KeyError:
        await message.delete()
        await ctx.respond("No data found try again...")
        


@plugin.command
@lightbulb.set_help("Get the steps and solution of a equation")
@lightbulb.option("equation", "Equation to solve")
@lightbulb.command(name="eq", aliases=("equ",), description="Calculate a equation")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_c(ctx: lightbulb.SlashContext) -> None:
    equation = ctx.options.equation
    query = urllib.parse.quote_plus(f"solve {equation}")
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={app_id}" \
                f"&input={query}" \
                f"&scanner=Solve" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=plaintext" \
                f"&output=json"

    r = requests.get(query_url).json()

    data = r["queryresult"]["pods"][0]["subpods"]
    result = data[0]["plaintext"]
    steps = data[1]["plaintext"]

    await ctx.respond(f"Result of {equation} is '{result}'.\n")
    await ctx.respond(f"> Possible steps to solution:\n\n{steps}")

@plugin.command
@lightbulb.set_help("Convert a plain text to LaTeX")
@lightbulb.option("expression", "Math expression to convert")
@lightbulb.command(name="f", aliases=("Lat",), description="Convert math expression to LaTeX")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_latex(ctx: lightbulb.SlashContext) -> None:
    embed = (hikari.Embed(
        color=Color(0x36393f),
    )
    .set_image("https://latex.codecogs.com/png.image?\dpi{190}&space;" + str(ctx.options.expression))
    )

    await ctx.respond(embed)
    
@plugin.command
@lightbulb.set_help("Basic Calculator.")
@lightbulb.option("calc", "The calc you need result")
@lightbulb.command(name="calc", description="Make basic calculations.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_calc(ctx: lightbulb.SlashContext) -> None:
    try:
        option = ctx.options.calc
        parse = ast.parse(option, mode="eval")
        for node in ast.walk(parse):
            print(type(node))
            if type(node) is ast.Call:
                await ctx.respond("Not valid operation in addition to detecting malicious code this will be reported")
                return

        result = (eval(compile(parse, "<string>", "eval")))
        await ctx.respond(f"Result: ```{result}```")
    except TypeError:
        await ctx.respond(f"{option} is a not valid math operation.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)