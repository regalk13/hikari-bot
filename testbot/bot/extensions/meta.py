from __future__ import annotations


import hikari
import lightbulb
import datetime as dt
from testbot.bot import Bot

import typing as t
class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def command_ping(self, ctx: lightbulb.Context) -> None:
        """Look at the latency of the bot."""
        await ctx.respond(f"Pong! Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")


    @lightbulb.command(name="userinfo", aliases=("ui", "info", "user"))
    async def command_userinfo(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        target = target or ctx.member


        embed = (hikari.Embed(
            title="User information.",
            description=f"Displaying information for {target.mention}",
            colour=target.colour,
            timestamp=dt.datetime.now().astimezone()

        )
        .set_author(name="Information")
        .set_footer(text=f"Requestest by {ctx.member.display_name}")
        .add_field(name="Test", value="Test")
    )
    
        await ctx.response(embed=embed)


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")