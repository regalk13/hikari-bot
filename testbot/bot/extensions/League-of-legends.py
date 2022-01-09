import hikari
from hikari.errors import HTTPError
import lightbulb
import requests
from hikari.colors import Color
from riotwatcher import LolWatcher, ApiError

plugin = lightbulb.Plugin(name="LoL", description="League of Legends summoner and champs stats.")

def data_version() -> str:
    ddragon = "https://ddragon.leagueoflegends.com/realms/euw.json"
    euw_json = requests.get(ddragon).json()
    return euw_json['n']['champion']

def build_data_url() -> str:
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

def row_headings() -> list:
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


@plugin.command
@lightbulb.set_help("Get information about a Lol summoner.")
@lightbulb.option("summoner", "Summoner you need the info.")
@lightbulb.command(name="summoner", description="Give you Lol summoner stats.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def cmd_summoner(ctx: lightbulb.SlashContext) -> None:
    with open("./secrets/api-key-riot", "r") as f:
        api_key = f.readline()
    watcher = LolWatcher(api_key)
    my_region = 'la1'
    try:
        me = watcher.summoner.by_name(my_region, ctx.options.summoner)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
            return
        elif err.response.status_code == 404:
            await ctx.respond('Summoner with that name not found.')
            return

        #elif err.response.status_code == 403:
        #    await ctx.respond("The api has problems to give results try again later")
        #    return
        else:
            raise
            return
    
    except HTTPError:
        await ctx.respond('Summoner with that name not found.')
        return

    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    #print(my_ranked_stats)
    try:
        embed = (hikari.Embed(
            color=Color(0x36393f)

        )
        .set_author(name=my_ranked_stats[0]['summonerName'], icon=f"http://ddragon.leagueoflegends.com/cdn/12.1.1/img/profileicon/{me['profileIconId']}.png")
        .set_thumbnail(f"http://ddragon.leagueoflegends.com/cdn/12.1.1/img/profileicon/{me['profileIconId']}.png")
        .add_field(name="<:LoL:929742706131996672> Level", value=f"``{me['summonerLevel']}``")
        )

        try:
            if my_ranked_stats[1]['tier'] == 'IRON':
                embed.add_field(name="<:Iron:929734011947995166> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``", inline=True)
            elif my_ranked_stats[1]['tier'] == 'BRONZE':
                embed.add_field(name="<:Bronze:929734304983023637> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``",inline=True)
            elif my_ranked_stats[1]['tier'] == 'SILVER':
                embed.add_field(name="<:Silver:929734330438279218> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``",inline=True)
            elif my_ranked_stats[1]['tier'] == 'GOLD':
                embed.add_field(name="<:Gold:929734354190602260> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``",inline=True)
            elif my_ranked_stats[1]['tier'] == 'PLATINUM':
                embed.add_field(name="<:Platinum:929734376688844862> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``",inline=True)
            elif my_ranked_stats[1]['tier'] == 'DIAMOND':
                embed.add_field(name="<:Diamond:929734505781166090> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``",inline=True)
            elif my_ranked_stats[1]['tier'] == 'MASTER':
                embed.add_field(name=" <:Master:929734551939461161> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``", inline=True)
            elif my_ranked_stats[1]['tier'] == 'GRANDMASTER':
                embed.add_field(name="<:GrandMaster:929734576178364497> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``", inline=True)
            elif my_ranked_stats[1]['tier'] == 'CHALLENGER':
                embed.add_field(name="<:Challenger:929734607727894548> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``", inline=True)
            else:
                embed.add_field(name="<:Iron:929734011947995166> Ranked (Solo/Duo)", value=f"> ``{my_ranked_stats[1]['tier']} {my_ranked_stats[1]['rank']}``", inline=True)

        except KeyError:
            if my_ranked_stats[0]['tier'] == 'IRON':
                embed.add_field(name="<:Iron:929734011947995166> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'BRONZE':
                embed.add_field(name="<:Bronze:929734304983023637> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'SILVER':
                embed.add_field(name="<:Silver:929734330438279218> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'GOLD':
                embed.add_field(name="<:Gold:929734354190602260> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'PLATINUM':
                embed.add_field(name="<:Platinum:929734376688844862> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'DIAMOND':
                embed.add_field(name="<:Diamond:929734505781166090> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'MASTER':
                embed.add_field(name=" <:Master:929734551939461161> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'GRANDMASTER':
                embed.add_field(name="<:GrandMaster:929734576178364497> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            elif my_ranked_stats[0]['tier'] == 'CHALLENGER':
                embed.add_field(name="<:Challenger:929734607727894548> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)
            else:
                embed.add_field(name="<:Iron:929734011947995166> Ranked (5vs5)", value=f"> ``{my_ranked_stats[0]['tier']} {my_ranked_stats[0]['rank']}``", inline=True)


        embed.add_field(name="<:Spell:928763270452613120> League Points", value=f"> ``{my_ranked_stats[1]['leaguePoints']}``", inline=True)
        embed.add_field(name="<:Bee:929744125136367699> Ranked wins", value=f"> ``{my_ranked_stats[1]['wins']}``", inline=False)
        embed.add_field(name="<:Lose:929744350261415997> Ranked lose", value=f"> ``{my_ranked_stats[1]['losses']}``", inline=False)

        await ctx.respond(embed)

    except IndexError:
        embed = (hikari.Embed(
            color=Color(0x36393f),
        )
        .set_author(name=me['name'], icon=f"http://ddragon.leagueoflegends.com/cdn/12.1.1/img/profileicon/{me['profileIconId']}.png")
        .set_thumbnail(f"http://ddragon.leagueoflegends.com/cdn/12.1.1/img/profileicon/{me['profileIconId']}.png")
        .add_field(name="<:LoL:929742706131996672> Level", value=f"``{me['summonerLevel']}``")
        .add_field(name="<:Iron:929734011947995166> Ranked", value="> ``UNRANKED``", inline=True)
        .add_field(name="<:Spell:928763270452613120> League Points", value="> ``Not Valid``", inline=True)
        .add_field(name="<:Bee:929744125136367699> Ranked wins", value="> ``Not Valid``", inline=False)
        .add_field(name="<:Lose:929744350261415997> Ranked lose", value="> ``Not Valid``", inline=False)
        )

        await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)