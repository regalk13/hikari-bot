from os import RTLD_GLOBAL
import hikari
from hikari.colors import Color
import lightbulb
import datetime as dt
from testbot.bot import Bot
import random 

import typing as t
class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        """Look at the latency of the bot."""
        await ctx.respond(f"Pong! Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")


    @lightbulb.command(name="userinfo", aliases=("ui", "info", "user"))
    async def command_userinfo(self, ctx: lightbulb.Context, *,  target: lightbulb.member_converter = None) -> None:
        """Look at the information of a user, empty argument represents see your own info."""
        target = target or ctx.member
        roles = []
        u_roles = ""
        for role in target.get_roles():
            roles.append(role.mention)

        for r in roles:
            u_roles += r

        r_g = random.randint(1, 255)
        r_b = random.randint(1, 255)
        r_r = random.randint(1, 255)

        embed = (hikari.Embed(
            title="User information.",
            description=f"Displaying information for {target.mention}",
            colour=Color.from_rgb(r_r, r_b, r_g),
            timestamp=dt.datetime.now().astimezone()
        )
        .set_author(name="Information")
        .set_footer(text=f"Requestest by {ctx.member.display_name}")
        .add_field(name="Created at", value=target.created_at.strftime("%b %d,%Y  %H:%M:%S"), inline=False)
        .add_field(name="Joined at", value=target.joined_at.strftime("%b %d,%Y  %H:%M:%S"))
        .add_field(name="Roles", value=u_roles)
        .set_thumbnail(target.avatar_url)
    )
    
        await ctx.respond(embed=embed)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")