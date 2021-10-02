from os import RTLD_GLOBAL, replace
import hikari
from hikari.colors import Color
import lightbulb
import datetime as dt
from datetime import datetime, timedelta

import psutil
from testbot.bot import Bot
import random 
from platform import python_version
from psutil import Process, cpu_times, virtual_memory
import typing as t
class Meta(lightbulb.Plugin):
    def __init__(self, bot: Bot):
        super().__init__(name="Meta")
        self.bot = bot


    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        """Look at the latency of the bot."""
        await ctx.respond(f"Pong! Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")


    @lightbulb.command(name="userinfo", aliases=("ui", "info", "user"))
    async def command_userinfo(self, ctx: lightbulb.Context, *,  target: lightbulb.member_converter = None) -> None:
        """Look at the information of a user, empty argument represents see your own info."""
        target = target or ctx.member
        roles = []
        for role in target.get_roles():
            roles.append(role.mention)

        u_roles = ", ".join(roles)
    

        r_g = random.randint(1, 255)
        r_b = random.randint(1, 255)
        r_r = random.randint(1, 255)

        
        presence = target.get_presence()
        if presence is None:
            activity_ = "No activity."

        else:
            activitys = []
            for activity in presence.activities:
                activitys.append(activity.name)


            activity_ = ', '.join(activitys)

        embed = (hikari.Embed(
            title="User information",
            description=f"Displaying information for {target.mention}",
            colour=Color.from_rgb(r_r, r_b, r_g),
            timestamp=dt.datetime.now().astimezone()
        )
        .set_author(name="Information")
        .set_footer(text=f"Requestest by {ctx.member.display_name}", icon=ctx.member.avatar_url)
        .add_field(name="<:ID:893578566296555520>", value=target.id)
        .add_field(name="<:User:893597475867336795> Discriminator", value=target.discriminator, inline=True)
        .add_field(name="<:Bot:893579925892767784> Bot?", value=target.is_bot, inline=True)
        .add_field(name="<:Role:893595137387675658> No. of roles", value=len(target.role_ids), inline=True)
        .add_field(name="<:New:893595680306774047> Created at", value=target.created_at.strftime("%b %d,%Y  %H:%M:%S"), inline=True)
        .add_field(name="<:Join:893595887853506600> Joined at", value=target.joined_at.strftime("%b %d,%Y  %H:%M:%S"), inline=True)
        .add_field(
            name="<:Boost:893579717821755402> Boosted since",
            value=getattr(target.premium_since, "strftime", lambda x: "Not boosting")("%d %b %Y"),
            inline=True
        )       

        .add_field(
            name="<:Info:893583131536412772> Roles",
            value=u_roles
        ) 


        .add_field(name="<:Presence:893596200148811776> Presence", 
        value=activity_)
        #.add_field(name="Roles", value=" | ".join(r.mention for r in reversed(target.role_ids[1:])))
        
        .set_thumbnail(target.avatar_url)
    )
    
        await ctx.respond(embed=embed, reply=True)



    @lightbulb.command(name="serverinfo", aliases=("guildinfo",))
    async def command_severinfo(self, ctx: lightbulb.Context) -> None:
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)

        owner = guild.get_member(guild.owner_id)

        channels = 0  
        bots = 0
        for channel in guild.get_channels().values():
            channels += 1
              
        for member in guild.get_members().values():
            if member.is_bot:
                bots += 1


        embed = (hikari.Embed(
            title=f"Server Information",
            description=guild.description,
            colour=Color(0x36393f),
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


    @lightbulb.command(name="pfp", aliases=("picture"))
    async def command_pfp(self, ctx: lightbulb.Context, *, target: lightbulb.member_converter = None) -> None:
        target = target or ctx.member
        image = target.avatar_url

        embed = (hikari.Embed(
            colour=Color(0x36393f),
            description=f"[Image]({image})",
        )
        .set_author(name=f"{target.username}#{target.discriminator}", icon=target.avatar_url)
        .set_image(image)
        )

        await ctx.respond(embed=embed, reply=True)


    @lightbulb.command(name="botinfo", aliases=("bi",))
    async def command_botinfo(self, ctx: lightbulb.Context) -> None:
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)

        r_g = random.randint(1, 255)
        r_b = random.randint(1, 255)
        r_r = random.randint(1, 255)

        proc = Process()
        with proc.oneshot():
            cpu_time = psutil.cpu_percent()
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        bots = guild.get_member(892053033792454727)
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
        .add_field(name="<:Bot:893579925892767784> Lightbulb Version", value="> 1.4.1", inline=True)
        .add_field(name="<:Devs:893886631017345064> Devs", value="> Lesly❁#9306 \n > Regalk#1654", inline=True)
        .add_field(name="<:Config:893582228246892554> CPU", value=f"> {cpu_time}%", inline=True)
        .add_field(name="<:Presence:893596200148811776> Memory Used", value=f"> {mem_usage:,.3f} Mib", inline=True)
        .add_field(name="<:Members:893581084762185739> Users", value="> On test", inline=True)
        .add_field(name="<:Book:893580795111936050> Servers", value="> On test", inline=True)
        .add_field(name="<:New:893595680306774047> Create at", value="> ``01/08/2021``", inline=True)
        )

        await ctx.respond(embed, reply=True)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta(bot))

def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")