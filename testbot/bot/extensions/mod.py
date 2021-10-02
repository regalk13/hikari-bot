import asyncio
import lightbulb
import hikari 
from testbot.bot import Bot
from hikari.colors import Color
import datetime as dt

class Mod(lightbulb.Plugin):
    def __init__(self, bot: Bot):
        super().__init__(name="Mod")
        self.bot = bot

    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.KICK_MEMBERS))
    @lightbulb.command(name="kick")
    async def command_kick(self, ctx: lightbulb.Context, target: lightbulb.member_converter, reason="No Reason") -> None:
        """Look at the latency of the bot."""
        self.log_channel = await self.bot.rest.fetch_channel(887515478304624730)

        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)

        embed = (hikari.Embed(
                title="Member Kicked",
                colour=Color(0xff0000),
                timestamp=dt.datetime.now().astimezone()

        )
        .add_field(name="<:User:893597475867336795> Member", value=f"{target.mention}", inline=True)
        .add_field(name="<:Staff:893660996458147861> Kicked by", value=f"{ctx.author.mention}", inline=True)
        .add_field(name="<:Invite:893581721721770064> Reason", value=reason)
        .set_thumbnail(target.avatar_url)
        )
        
        await guild.kick(target)
        await self.log_channel.send(embed) 


    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
    @lightbulb.command(name="ban")
    async def command_ban(self, ctx: lightbulb.Context, target: lightbulb.member_converter, reason="No Reason") -> None:
        """Look at the latency of the bot."""
        self.log_channel = await self.bot.rest.fetch_channel(887515478304624730)

        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)

        embed = (hikari.Embed(
                title="Member Banned",
                colour=Color(0xff0000),
                timestamp=dt.datetime.now().astimezone()

        )
        .add_field(name="<:User:893597475867336795> Member", value=f"{target.mention}", inline=True)
        .add_field(name="<:Staff:893660996458147861> Banned by", value=f"{ctx.author.mention}", inline=True)
        .add_field(name="<:Invite:893581721721770064> Reason", value=reason)
        .set_thumbnail(target.avatar_url)
        )
        
        await guild.ban(target)
        await self.log_channel.send(embed) 

    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_MESSAGES))
    @lightbulb.command(name="clear", aliases=("purge",))
    async def command_clear(self, ctx: lightbulb.Context, limit: int = 1):        
        
        message = await ctx.respond(f"<a:Loading:893842133792997406> Deleting messages.")

        await self.bot.rest.delete_messages(ctx.channel_id, 893841545504108565, ctx.message_id)
        await self.bot.rest.edit_message(ctx.channel_id, message.id, content="<a:Right:893842032248885249> Message(s) deleted.")
        await asyncio.sleep(5)
        await self.bot.rest.delete_messages(ctx.channel_id, message.id)


def load(bot: Bot) -> None:
    bot.add_plugin(Mod(bot))

def unload(bot: Bot) -> None:
    bot.remove_plugin("Mod")
