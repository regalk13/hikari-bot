import lightbulb
import hikari
import requests
from hikari.colors import Color
from lightbulb.errors import LightbulbError
from testbot.bot import Bot
import random
import json

plugin = lightbulb.Plugin(name="Actions", description="Multiple actions to perform between users.")

    
def get_gif(term) -> str:
    api_key = "36SW53ZHFSNF"
    limit = 14
    
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (term, api_key, limit))


    gifs_data = json.loads(r.content)
    gif = gifs_data["results"][random.randint(0,13)]["media"][0]["gif"]["url"]

    return gif



async def action(ctx: lightbulb.Context, text, image) -> None:
    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    embed = (hikari.Embed(
        description=f"{text}",
        colour=Color.from_rgb(r_g, r_b, r_r)
    )
    .set_image(image)
    )

    await ctx.respond(embed)

@plugin.command
@lightbulb.set_help("With this command you can kiss the person who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("kiss", "Kiss someone.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_kiss(ctx: lightbulb.context):
    
    target = ctx.options.member

    gif = get_gif("anime-kiss")
    await action(ctx, f"**{ctx.member.username}** le dio un beso a **{target.username}**. (づ￣ ³￣)づ", gif)



def load(bot: Bot) -> None:
    bot.add_plugin(plugin)

def unload(bot: Bot) -> None:
    bot.remove_plugin(plugin)