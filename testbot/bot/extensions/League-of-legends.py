import hikari
import lightbulb
import requests
from hikari.colors import Color

plugin = lightbulb.Plugin(name="Lol", description="League of Legends summoner and champs stats.")

def data_version():
    ddragon = "https://ddragon.leagueoflegends.com/realms/euw.json"
    euw_json = requests.get(ddragon).json()
    return euw_json['n']['champion']


def build_data_url():
    return "http://ddragon.leagueoflegends.com/cdn/" + data_version() + "/data/en_GB/champion.json"


def get_jsons():
    data_url = build_data_url()
    data_json = requests.get(data_url).json()
    champ_list = data_json['data'].keys()
    return data_json, champ_list


# Not used, but could be implemented to calculate stats at different levels
def level_math(base, per_level, level):
    level_stat = base + (per_level * level)
    return level_stat


def row_headings():
    return [
        "Name",
        "HP",
        "HP Per Level",
        "MP",
        "MP Per Level",
        "Move Speed",
        "Armor",
        "Armour Per Level",
        "Spell Block",
        "Spell Block Per Level",
        "Attack Range",
        "HP Regen",
        "HP Regen Per Level",
        "MP Regen",
        "MP Regen Per Level",
        "Attack Damage",
        "Attack Damage Per Level",
        "Attack Speed",
        "Attack Speed Per Level"
    ]   

@plugin.command()
@lightbulb.set_help("Get stats of a league of legends champion (using riot API)")
@lightbulb.option("champ", "Champ you want stats")
@lightbulb.command(name="stats_lol", description="Get champ stats")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def command_stats(ctx: lightbulb.SlashContext) -> None:
    data_json, champ_list = get_jsons()
    champ = str(ctx.options.champ)
    try:
        name = data_json['data'][champ]['name']
        description = data_json['data'][champ]['title']
        hp = data_json['data'][champ]['stats']['hp']
        hpperlevel = data_json['data'][champ]['stats']['hpperlevel']
        movespeed = data_json['data'][champ]['stats']['movespeed']
        armor = data_json['data'][champ]['stats']['armor']
        armorperlevel = data_json['data'][champ]['stats']['armorperlevel']
        attackspeed = data_json['data'][champ]['stats']['attackspeed']

        
        embed = (hikari.Embed(
            description=f"{description}.".title(),
            color=Color(0x36393f)
        )
        .set_author(name=f"{name}", icon=f"https://static.u.gg/assets/lol/riot_static/12.1.1/img/champion/{champ}.png", url=f"https://u.gg/lol/champions/{champ}/build".lower())
        .set_image(f"https://static.u.gg/assets/lol/riot_static/12.1.1/img/splash/{champ}_0.jpg")
        .add_field(name="<:Hp:928763481241579520> Hp", value=f"> {hp}", inline=True)
        .add_field(name="<:Hp:928763481241579520> Hp-Level", value=f"> {hpperlevel}", inline=True)
        .add_field(name="<:Spell:928763270452613120> Move Speed", value=f"> {movespeed}", inline=True)
        .add_field(name="<:Armor:928762943909265458> Armor", value=f"> {armor}", inline=True)
        .add_field(name="<:Armor2:928763869814476810> Armor-Level", value=f"> {armorperlevel}", inline=True)
        .add_field(name="<:Attack:928762228407169086> Attack Speed", value=f"> {attackspeed}", inline=True)
        )
        
        await ctx.respond(embed)

    except KeyError:
        await ctx.respond("Champ dont found...")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)