from re import L
import lightbulb
import hikari
import requests
from hikari.colors import Color
import random
import json

plugin = lightbulb.Plugin(name="Actions", description="Multiple actions or reactions to perform between users.")
#Implements all actions-reactions commands of Nekotina bot in hikari 
    
def get_gif(term, limit = 14) -> str:
    api_key = "36SW53ZHFSNF"
    limit = limit
    
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (term, api_key, limit))


    gifs_data = json.loads(r.content)
    gif = gifs_data["results"][random.randint(0,limit-1)]["media"][0]["gif"]["url"]

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
@lightbulb.set_help("Kiss the person who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("kiss", "Kiss someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_kiss(ctx: lightbulb.context):
    target = ctx.options.member
    if target.id == ctx.member.id:
        await ctx.respond(f"I don't think you can kiss yourself {ctx.member.mention}")
        return

    gif = get_gif("anime-kiss")
    await action(ctx, f"**{ctx.member.username}** le dio un beso a **{target.username}**. (づ￣ ³￣)づ", gif)

@plugin.command
@lightbulb.set_help("Clap or clap for someone.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("clap", "Just clap or clap for someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_clap(ctx: lightbulb.context):
    
    target = ctx.options.member

    gif = get_gif("anime-clap")

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is clapping", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** applauds **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Get angry with or without a person you mention.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("angry", "Shows anger at someone or just angry.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_angry(ctx: lightbulb.context):
    
    target = ctx.options.member

    gif = get_gif("anime-angry")
    
    if target == None:
        await action(ctx, f"**{ctx.member.username}** got mad >:C", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** got mad with **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Highfive to the person who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("highfive", "Highfive to someone :)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_highfive(ctx: lightbulb.context):
    
    target = ctx.options.member

    gif = get_gif("anime-highfive")
    await action(ctx, f"**{ctx.member.username}** highfive to **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Laugh or tease someone you mention")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("laugh", "Laugh or tease.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_laugh(ctx: lightbulb.context):
    
    target = ctx.options.member

    gif = get_gif("anime-laugh")
    if target == None:
        await action(ctx, f"**{ctx.member.username}** is laughing.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** laughs at **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Throw some water in someone's face.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("splash", "Splash Splash!!! in someone :)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_splash(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-splash")

    await action(ctx, f"**{ctx.member.username}** splash to **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Be scared by something or by someone who mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("scare", "Show you are scared.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_scare(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-scare")

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is scared.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** scared by **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Be tsundere with someone or saiki will be tsundere with you iiii];)'")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("tsundere", "Tsundere to someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_tsundere(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-tsundere")

    if target == None:
        await action(ctx, f"¬¬ ¡Hmm! silly **{ctx.member.username}**", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** is being tsundere with **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Tell someone baka or saiki will say you baka!!!")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("baka", "Tell someone baka.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_baka(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-baka")
    
    if target == None:
        await action(ctx, f"**{ctx.member.username}** BAKA!!!", gif)

    else:
        await action(ctx, f"**{target.username}** BAKA!!!", gif)

@plugin.command
@lightbulb.set_help("Cook something for you or for someone.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("cook", "Cook something.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_cook(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-cook")

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is cooking something delicious.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** is cooking something delicious for **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Show you are changing the world whit code.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("program", "Programming alone or with someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_program(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-programmer", limit=3)

    if target == None:
        await action(ctx, f"**{ctx.member.username}** is programming something amazing.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** is programming something amazing with **{target.username}**", gif)


@plugin.command
@lightbulb.set_help("Take the hands of the person who mention or saiki hands.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("handholding", "Take someone's hand.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_handholding(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-handholding")

    if target == None:
        await action(ctx, f"**{ctx.member.username}** take my hand.", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** hand holding with **{target.username}**", gif)

@plugin.command
@lightbulb.set_help("Give a hug to whoever mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("hug", "Just hug someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_hug(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-hug")

    await action(ctx, f"**{ctx.member.username}** hug to **{target.username}**", gif)


@plugin.command
@lightbulb.set_help("lick to whoever mentions.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("lick", "can you lick someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_lick(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-lick")

    await action(ctx, f"**{ctx.member.username}** lick to **{target.username}**", gif)


@plugin.command
@lightbulb.set_help("Shoot whoever mentions or saiki will shoot you.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member, required=False)
@lightbulb.command("shoot", "Shoot someone")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_kiss(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-shoot")

    if target == None:
        await action(ctx, f"**Saiki** shoot to **{ctx.member.username}**", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** shoot to **{target.username}**", gif)


@plugin.command
@lightbulb.set_help("Send someone away with your spray or saiki will use his.")
@lightbulb.option("member", "The member you choice for make the action.", hikari.Member)
@lightbulb.command("spray", "Spray someone.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_kiss(ctx: lightbulb.context):
    target = ctx.options.member
    gif = get_gif("anime-spray")
    
    if target == None:
        await action(ctx, f"**Saiki** spray to **{ctx.member.username}**", gif)

    else:
        await action(ctx, f"**{ctx.member.username}** spray to **{target.username}**", gif)



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)