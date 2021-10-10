import asyncio
import logging
from hikari import PermissionOverwrite, PermissionOverwriteType
from hikari.permissions import Permissions
import lightbulb
import hikari 
from testbot.bot import Bot
from hikari.colors import Color
import datetime as dt
from datetime import datetime, timedelta

class Mod(lightbulb.Plugin):
    def __init__(self, bot: Bot):
        super().__init__(name="Mod")
        self.bot = bot

    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.KICK_MEMBERS))
    @lightbulb.command(name="kick")
    async def command_kick(self, ctx: lightbulb.Context, target: lightbulb.member_converter, *, reason="No Reason") -> None:
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
    async def command_ban(self, ctx: lightbulb.Context, target: lightbulb.member_converter, *, reason="No Reason") -> None:
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
        

    
    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
    @lightbulb.command(name="unban")
    async def command_unban(self, ctx: lightbulb.Context, target: lightbulb.member_converter, *, reason="No Reason") -> None:
        """Look at the latency of the bot."""
        self.log_channel = await self.bot.rest.fetch_channel(887515478304624730)

        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)

        embed = (hikari.Embed(
                title="Member Unbanned",
                colour=Color(0xff0000),
                timestamp=dt.datetime.now().astimezone()

        )
        .add_field(name="<:User:893597475867336795> Member", value=f"{target.mention}", inline=True)
        .add_field(name="<:Staff:893660996458147861> Unanned by", value=f"{ctx.author.mention}", inline=True)
        .add_field(name="<:Invite:893581721721770064> Reason", value=reason)
        .set_thumbnail(target.avatar_url)
        )
        
        await guild.unban(target)
        await self.log_channel.send(embed) 

    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_MESSAGES))
    @lightbulb.command(name="clear", aliases=("purge",))
    async def command_clear(self, ctx: lightbulb.Context, limit: int = 1):

        if 0 < limit <= 100:
            if limit == 100:
                limit = limit - 1

            channel = await self.bot.rest.fetch_channel(ctx.channel_id)
            message = await ctx.respond(f"<a:Loading:893842133792997406> Deleting messages.")
            messages_ = []
            messages_dont = []

            async for messages in channel.fetch_history(before=ctx.timestamp).limit(limit):
                    time_between_insertion = ctx.timestamp - messages.created_at
                    if time_between_insertion.days > 14:
                        messages_dont.append(messages)
                    else:
                        messages_.append(messages)

            if len(messages_dont) > 1:
                    await message.edit(content=f"<a:Wrong:893873540846198844> remember that I can only delete messages 14 days old, {len(messages_dont)} messages will be discarded.")
                    await asyncio.sleep(5)

            if len(messages_) > 1:
                await self.bot.rest.delete_messages(ctx.channel_id, messages_, ctx.message_id)
                if limit == 100:
                    await message.edit(content=f"<a:Right:893842032248885249> {len(messages_)+1} Message(s) deleted.")

                await message.edit(content=f"<a:Right:893842032248885249> {len(messages_)} Message(s) deleted.")
                await asyncio.sleep(5)
                await message.delete()
            
            else:
                await message.edit(content=f"<a:Right:893842032248885249> {len(messages_)} Message(s) deleted.")
                await asyncio.sleep(5)
                await message.delete()

            
        else:
            await ctx.respond("<a:Wrong:893873540846198844> The number of messages you want to delete is not within the limits.")


    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
    @lightbulb.command(name="slowmode", aliases=("sm",))
    async def command_slowmode(self, ctx: lightbulb.Context, time):
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)
        channel = guild.get_channel(ctx.channel_id)

        time_converter = list(time)
        time_ = 0

        if len(time_converter) >= 2: 

            if time_converter[1] == "s":
                time_ = int(time_converter[0])
                message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {time} applied.")


            elif time_converter[1] == "m":
                time_ = int(time_converter[0]) * 60
                message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {time} applied.")


            elif time_converter[1] == "h":
                time_ = int(time_converter[0]) * 3600
                message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {time} applied.")

            else:
                message = await ctx.respond("``Valid format: (time)s, (time)m, (time)h``")   

        else:
            message = await ctx.respond("``Valid format: (time)s, (time)m, (time)h``")     


        await channel.edit(rate_limit_per_user=int(time_))
        await asyncio.sleep(5)
        await message.delete()


    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
    @lightbulb.command(name="lock", aliases=("lck",))
    async def command_lock(self, ctx: lightbulb.Context):
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)
        channel_ = guild.get_channel(ctx.channel_id)

        id_role = ""
        for role in member.get_roles():
            if role.name == "@everyone":
                id_role = role.id


        await self.bot.rest.edit_permission_overwrites(
            channel = channel_,
            target_type = PermissionOverwriteType.ROLE,
            target=id_role,
            allow=(
            Permissions.VIEW_CHANNEL
            | Permissions.READ_MESSAGE_HISTORY
            ),
            deny=(
            Permissions.VIEW_CHANNEL
            | Permissions.SEND_MESSAGES
            )
        )    
        await ctx.respond(f"<a:Right:893842032248885249> channel locked...")


    @lightbulb.check(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
    @lightbulb.command(name="unlock", aliases=("ulck",))
    async def command_unlock(self, ctx: lightbulb.Context):
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)
        channel_ = guild.get_channel(ctx.channel_id)

        id_role = ""
        for role in member.get_roles():
            if role.name == "@everyone":
                id_role = role.id


        await self.bot.rest.edit_permission_overwrites(
            channel = channel_,
            target_type = PermissionOverwriteType.ROLE,
            target=id_role,
            allow=(
            Permissions.VIEW_CHANNEL
            | Permissions.READ_MESSAGE_HISTORY
            | Permissions.SEND_MESSAGES
            ),
            deny=(
            Permissions.MANAGE_MESSAGES
            | Permissions.SPEAK
            )
        )    
        await ctx.respond(f"<a:Right:893842032248885249> channel unlocked...")
    
def load(bot: Bot) -> None:
    bot.add_plugin(Mod(bot))

def unload(bot: Bot) -> None:
    bot.remove_plugin("Mod")
