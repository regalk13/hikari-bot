import asyncio
import logging
from typing import DefaultDict
from hikari import PermissionOverwrite, PermissionOverwriteType
from hikari.permissions import Permissions
import lightbulb
import hikari 
from hikari.colors import Color
import datetime as dt
from datetime import datetime, timedelta

from lightbulb.commands import prefix

plugin = lightbulb.Plugin(name="Mod", description="Commands for moderation (Need permissions)")

@plugin.command
@lightbulb.set_help("If the user has the same or higher permissions, it will not be possible to kick it.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option("target", "Target you will kick", hikari.Member)
@lightbulb.option("reason", "Reason for the kick", default="No reason")
@lightbulb.command(name="kick", description="Kick the target you mention.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_kick(ctx: lightbulb.SlashContext) -> None:
    log_channel = await plugin.bot.rest.fetch_channel(887515478304624730)
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)

    print(ctx.options.target)
    embed = (hikari.Embed(
            title="Member Kicked",
            colour=Color(0xff0000),
            timestamp=dt.datetime.now().astimezone()

    )
    .add_field(name="<:User:893597475867336795> Member", value=f"{ctx.options.target.mention}", inline=True)
    .add_field(name="<:Staff:893660996458147861> Kicked by", value=f"{ctx.author.mention}", inline=True)
    .add_field(name="<:Invite:893581721721770064> Reason", value=ctx.options.reason)
    .set_thumbnail(ctx.options.target.avatar_url)
    )
        
    await guild.kick(ctx.options.target)
    await log_channel.send(embed) 

@plugin.command
@lightbulb.set_help("If the user has the same of higher permissions, it will not be possible to ban it.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("target", "Target you will ban", hikari.Member)
@lightbulb.option("reason", "Reason for the ban", default="No reason")
@lightbulb.command(name="ban", description="Ban the target you mention.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_ban(ctx: lightbulb.SlashContext) -> None:    
    log_channel = await plugin.bot.rest.fetch_channel(887515478304624730)

    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)

    embed = (hikari.Embed(
            title="Member Banned",
            colour=Color(0xff0000),
            timestamp=dt.datetime.now().astimezone()
    )
    .add_field(name="<:User:893597475867336795> Member", value=f"{ctx.options.target.mention}", inline=True)
    .add_field(name="<:Staff:893660996458147861> Banned by", value=f"{ctx.author.mention}", inline=True)
    .add_field(name="<:Invite:893581721721770064> Reason", value=ctx.options.reason)
    .set_thumbnail(ctx.options.target.avatar_url)
    )
        
    await guild.ban(ctx.options.target)
    await log_channel.send(embed)
        
@plugin.command
@lightbulb.set_help("You can only unban those who are banned")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("target", "Target you will unban", hikari.Member)
@lightbulb.option("reason", "Reason for the unban", default="No reason")
@lightbulb.command(name="unban", description="Unban a banned user.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_unban(ctx: lightbulb.SlashContext) -> None:
    log_channel = await plugin.bot.rest.fetch_channel(887515478304624730)

    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)

    embed = (hikari.Embed(
            title="Member Unbanned",
            colour=Color(0xff0000),
            timestamp=dt.datetime.now().astimezone()
    )
    .add_field(name="<:User:893597475867336795> Member", value=f"{ctx.options.target.mention}", inline=True)
    .add_field(name="<:Staff:893660996458147861> Unanned by", value=f"{ctx.author.mention}", inline=True)
    .add_field(name="<:Invite:893581721721770064> Reason", value=ctx.options.reason)
    .set_thumbnail(ctx.options.target.avatar_url)
    )    
    await guild.unban(ctx.options.target)
    await log_channel.send(embed) 

@plugin.command
@lightbulb.set_help("The limit for clear messages is 100 and messages of the last 15 days.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("limit", "Limit of delete messages", int, default=2)
#@lightbulb.option("user", "The user for delete messages", required=False)
@lightbulb.command(name="clear", aliases=("purge",), description="Clear messages")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def purge(ctx: lightbulb.SlashContext):
    if ctx.options.amount < 2:
        return await ctx.respond("I cant purge less then 2 messages >:(")
    elif ctx.options.amount > 100:
        return await ctx.respond("I cant purge more the 100 messages!")
    #if not ctx.option.user:
    channel = await plugin.bot.rest.fetch_channel(ctx.channel_id)

    async for messages in channel.fetch_history(before=ctx.timestamp).limit(ctx.options.limit):
        print(messages)



    await ctx.respond("<a:Right:893842032248885249> {len(messages_)} Message(s) deleted")
    #else:
    #    def purge_type(m):
    #        return m.author == ctx.option.user

    #    await ctx.channel.purge(limit=ctx.options.amount+1, check=purge_type)
    #    await ctx.respond("<a:Right:893842032248885249> {len(messages_)} Message(s) deleted")
            


@plugin.command
@lightbulb.set_help("Add slowmode to the channel: 1s = 1 second, 1m = 1 minute, 1h = 1 hour. Max 6 hours.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.option("time", "Time to add slowmode")
@lightbulb.command(name="slowmode", aliases=("sm",), description="Add slowmode to the channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_slowmode(ctx: lightbulb.SlashContext):
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)
    channel = guild.get_channel(ctx.channel_id)

    time_converter = list(ctx.options.time)
    time_ = 0

    if len(time_converter) >= 2: 

        if time_converter[1] == "s":
            time_ = int(time_converter[0])
            message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {ctx.options.time} applied.")


        elif time_converter[1] == "m":
            time_ = int(time_converter[0]) * 60
            message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {ctx.options.time} applied.")


        elif time_converter[1] == "h":
            time_ = int(time_converter[0]) * 3600
            message = await ctx.respond(f"<a:Right:893842032248885249> slowmode of {ctx.options.time} applied.")

        else:
            message = await ctx.respond("``Valid format: (time)s, (time)m, (time)h``")   

    else:
        message = await ctx.respond("``Valid format: (time)s, (time)m, (time)h``")     


    await channel.edit(rate_limit_per_user=int(time_))
    await asyncio.sleep(5)
    await message.delete()

@plugin.command
@lightbulb.set_help("Lock the channel, just roles with admin persmissions can use the channel.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.command(name="unlock", aliases=("ulck",), description="Lock the channel for moderation.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_unlock(ctx: lightbulb.SlashContext):
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)
    channel_ = guild.get_channel(ctx.channel_id)

    id_role = ""
    for role in member.get_roles():
        if role.name == "@everyone":
            id_role = role.id


    await plugin.bot.rest.edit_permission_overwrites(
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
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)