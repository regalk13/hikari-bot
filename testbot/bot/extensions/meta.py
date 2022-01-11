from re import L
import hikari
from hikari.colors import Color
from hikari.messages import ButtonStyle
import lightbulb
import datetime as dt
from lightbulb.commands import user

import psutil
import random 
from platform import libc_ver, python_version
from psutil import Process, virtual_memory
import typing as t

plugin = lightbulb.Plugin(name="Meta", description="Information about the bot, users and servers.")


@plugin.command()
@lightbulb.set_help("Get the right stats of the bot ping")
@lightbulb.command(name="ping", description="Get the ping of bot")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"Pong! Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

@plugin.command()
@lightbulb.set_help("If you don't mention anybody, will show your own user info.")
@lightbulb.option("target", "target you want info", hikari.Member, required=False)
@lightbulb.command(name="userinfo", aliases=("ui", "info", "user"), description="Get the userinfo of whoever you mention")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_userinfo(ctx: lightbulb.SlashContext) -> None:
    target = ctx.options.target or ctx.member
    roles = []
    fetch_target = plugin.bot.cache.get_user(target.id)


    for role in target.get_roles():    
        roles.append(role.mention)
        
    if len(roles) > 25:
        u_roles = ", ".join(roles[:25])

    else: 
        u_roles = ", ".join(roles)
        
    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)


    activity_ = "No activity."
    presence = target.get_presence()
    if presence == None:
        activity_ = "No activity."

    else:
        if presence.activities == []:
            activity_ = "No activity."

        else:
            activitys = []
            for activity in presence.activities:
                activitys.append(activity.name)


            activity_ = ', '.join(activitys)

    accent_colour = str(fetch_target.accent_color)[1:]
     
    userinfo = await ctx.bot.d.db.try_fetch_record(
        "SELECT cookies, descrip FROM user WHERE user_id = ?",
        target.id,
    )


    if not target.is_bot:
        description_user = userinfo.descrip
        cookie = userinfo.cookies

    else:
        description_user = f"Displaying information for {target.mention}"
        cookie = "Not valid."

    embed = (hikari.Embed(
        title=f"{target.username}'s Information",
        description=description_user,
        colour=Color.from_rgb(r_r, r_b, r_g),
        timestamp=dt.datetime.now().astimezone()
    )
    .set_image(fetch_target.banner_url or f"https://singlecolorimage.com/get/{accent_colour}/400x100")
    .set_author(name="Information")
    .set_footer(text=f"Requestest by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    .add_field(name="<:ID:893578566296555520>", value=target.id, inline=False)
    .add_field(name="<:User:893597475867336795> Discriminator", value=target.discriminator, inline=False)
    .add_field(name="<:Bot:893579925892767784> Bot?", value=target.is_bot, inline=True)
    .add_field(name="<:Role:893595137387675658> No. of roles", value=len(target.role_ids), inline=True)
    .add_field(name="<:pepe_cookie:928678715309826098> Cookies", value=cookie, inline=True)
    .add_field(name="<:Join:893595887853506600> Joined at", value=f'``{target.joined_at.strftime("%b %d,%Y  %H:%M:%S")}``', inline=True)
    .add_field(name="<:New:893595680306774047> Created at", value=f'``{target.created_at.strftime("%b %d,%Y  %H:%M:%S")}``', inline=True)
    .add_field(
        name="<:Boost:893579717821755402> Boosting",
        value=getattr(target.premium_since, "strftime", lambda x: "Not boosting")("%d %b %Y"),
        inline=True
    )       
    .add_field(
        name="<:Info:893583131536412772> Roles",
        value=u_roles
    ) 
    .add_field(name="<:Presence:893596200148811776> Presence", 
        value=activity_)   
    .set_thumbnail(target.avatar_url)
    )
  

    await ctx.respond(embed=embed, reply=True)


@plugin.command()
@lightbulb.set_help("Get the info of the currently server.")
@lightbulb.command(name="serverinfo", aliases=("guildinfo", "si"), description="Get all the server information.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_severinfo(ctx: lightbulb.SlashContext) -> None:
    
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)


    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    owner = guild.get_member(guild.owner_id)

    channels = len(guild.get_channels().values())  
    bots = 0
              
    for member in guild.get_members().values():
        if member.is_bot:
            bots += 1


    embed = (hikari.Embed(
        title=f"Server Information",
        description=guild.description,
        colour=Color.from_rgb(r_r, r_b, r_g),
        timestamp=dt.datetime.now().astimezone()

    )
    .set_thumbnail(guild.icon_url)
    .set_footer(text=f"Requestest by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    .set_author(name=guild.name, icon=guild.icon_url)

    .add_field(name="<:ID:893578566296555520>", value=guild.id)
    .add_field(name="<:Owner:893579388774395964> Owner", value=owner.mention, inline=True)
    .add_field(name="<:Book:893580795111936050> Created", value=ctx.guild_id.created_at.strftime("%d/%m/%Y"), inline=True)
    .add_field(name="<:Members:893581084762185739> Members", value=guild.approximate_member_count, inline=True)
    .add_field(name="<:Bot:893579925892767784> Bots", value=bots, inline=True)
    .add_field(name="<:Config:893582228246892554> Channels", value=channels, inline=True)
    .add_field(name="<:Role:893595137387675658> Roles", value=len(guild.roles), inline=True)
    .add_field(name="<:Invite:893581721721770064> Invites", value=f"{len(ctx.bot.cache.get_invites_view_for_guild(guild)):,}", inline=True)
    .add_field(name="<:Emote:893580385261350953> Emotes", value=f"{len(guild.emojis):,}", inline=True)
    .add_field(name="<:Boost:893579717821755402> Boosts", value=guild.premium_subscription_count, inline=True)
    )

    await ctx.respond(embed, reply=True)

@plugin.command()
@lightbulb.set_help("Get the profile picture of the target or your own pfp")
@lightbulb.option("target", "target you want see the picture", hikari.Member, required=False)
@lightbulb.command(name="pfp", aliases=("picture"), description="Get the pfp of the target")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_pfp(ctx: lightbulb.SlashContext) -> None:    
    target = ctx.options.target or ctx.member
    image = target.avatar_url

    embed = (hikari.Embed(
        colour=Color(0x36393f),
        description=f"[Image]({image})",
    )
    .set_author(name=f"{target.username}#{target.discriminator}", icon=target.avatar_url)
    .set_image(image)
    )

    await ctx.respond(embed=embed, reply=True)

@plugin.command()
@lightbulb.set_help("Get all the bot information.")
@lightbulb.command(name="botinfo", aliases=("bi",), description="Use to see all info of saiki bot.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_botinfo(ctx: lightbulb.SlashContext) -> None:    
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)
    guilds = plugin.bot.cache.get_guilds_view()
    users = plugin.bot.cache.get_members_view()
        
    message = await ctx.respond("<a:Loading:893842133792997406> Loading data")    
    members = []
    for user in users:
        guild_ = await plugin.bot.rest.fetch_guild(user)
        for member in guild_.get_members().values():
            members.append(member)
    
    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    proc = Process()
    with proc.oneshot():
        cpu_time = psutil.cpu_percent()
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

    bots = guild.get_my_member()
    embed = (hikari.Embed(
        description="Saiki the best option",
        colour=Color.from_rgb(r_r,r_g,r_b),
        timestamp=dt.datetime.now().astimezone()
    )
    .set_author(name=f"{bots.username}#{bots.discriminator}", icon=bots.avatar_url)
    .set_thumbnail(bots.avatar_url)
        
    .set_footer(text=f"Requestest by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    .add_field(name="<:ID:893578566296555520>", value=f"{bots.id}")
    .add_field(name="<:Python:893887482016444416> Python Version", value=f"> {python_version()}", inline=True)
    .add_field(name="<:Hikari:893888774369591316> Hikari Version", value=f"> {hikari.__version__}", inline=True)
    .add_field(name="<:Bot:893579925892767784> Lightbulb Version", value="> 2.1.3", inline=True)
    .add_field(name="<:Devs:893886631017345064> Devs", value="> Lesly❁#9306 \n > Regalk#5910", inline=True)
    .add_field(name="<:Config:893582228246892554> CPU", value=f"> {cpu_time}%", inline=True)
    .add_field(name="<:Presence:893596200148811776> Memory Used", value=f"> {mem_usage:,.3f} Mib", inline=True)
    .add_field(name="<:Members:893581084762185739> Users", value=f"> {len(members)}", inline=True)
    .add_field(name="<:Book:893580795111936050> Servers", value=f"> {len(guilds)}", inline=True)
    .add_field(name="<:New:893595680306774047> Create at", value="> ``01/08/2021``", inline=True)
    )

    await message.delete()
    await ctx.respond(embed, reply=True)

@plugin.command()
@lightbulb.set_help("Set the message will appear in the command -ui.")
@lightbulb.option("message", "Message you want in to you user info.")
@lightbulb.command(name="setinfo", aliases=("setdesc",), description="Set the message you want in your user info.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_setter(ctx: lightbulb.SlashContext) -> None:
    await plugin.bot.d.db.execute(
        "UPDATE user SET descrip = ? WHERE user_id = ?",
        ctx.options.message, 
        ctx.member.id
    )
    await ctx.respond("<a:Right:893842032248885249> new user information updated successfully.")
   
@plugin.command()
@lightbulb.set_help("You can add the bot to your server whit this link.")
@lightbulb.command(name="invite", description="Get the invite link of the bot")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_invite(ctx: lightbulb.SlashContext) -> None:
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)
    bot = guild.get_my_member()
    componetens_ = plugin.bot.rest.build_action_row() 
    button = componetens_.add_button(ButtonStyle.LINK, f"https://discord.com/api/oauth2/authorize?client_id=892053033792454727&permissions=8&scope=bot%20applications.commands").set_label("Invite the bot").add_to_container()
        
    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)


    embed = (hikari.Embed(
        title="Bot invite",
        colour=Color.from_rgb(r_g, r_b, r_r),
        description="Click the button to invite the bot to your server."
    )
    .set_thumbnail(bot.avatar_url)
    )

    await ctx.respond(embed, component=button)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)