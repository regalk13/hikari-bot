import asyncio
import logging
from tarfile import ExFileObject
from typing import DefaultDict
from xml.dom import NotFoundErr
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
@lightbulb.implements(lightbulb.SlashCommand)
async def command_kick(ctx: lightbulb.SlashContext) -> None:
    log_channel_id = await plugin.bot.d.db.try_fetch_record("SELECT log_channel FROM guild WHERE guild_id = ?", ctx.guild_id)
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
       
       
    try:
        await guild.kick(ctx.options.target)
        if log_channel_id.log_channel == 0:
            await ctx.respond("<a:Right:893842032248885249> Member kicked, but you don't have a log channel use ``/log``.")  
            return

        try:
            log_channel = await plugin.bot.rest.fetch_channel(log_channel_id.log_channel)
            await log_channel.send(embed)
            await ctx.respond("<a:Right:893842032248885249> Member kicked.")  
            return

        except hikari.NotFoundError:
            await ctx.respond("<a:Right:893842032248885249> Member kicked, but you don't have a log channel use ``/log``.")  
            return


    except hikari.ForbiddenError:
        await ctx.respond("<a:Wrong:893873540846198844> I can't kick a admin user or more high role at me.")


@plugin.command
@lightbulb.set_help("If the user has the same of higher permissions, it will not be possible to ban it.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("target", "Target you will ban", hikari.Member)
@lightbulb.option("reason", "Reason for the ban", default="No reason")
@lightbulb.command(name="ban", description="Ban the target you mention.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_ban(ctx: lightbulb.SlashContext) -> None:  
    log_channel_id = await plugin.bot.d.db.try_fetch_record("SELECT log_channel FROM guild WHERE guild_id = ?", ctx.guild_id)
  

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
    
    try:
        await guild.ban(ctx.options.target, reason=ctx.options.reason, delete_message_days=7)
        if log_channel_id.log_channel == 0:
            await ctx.respond("<a:Right:893842032248885249> Member banned, but you don't have a log channel use ``/log``.")  
            return

        log_channel = await plugin.bot.rest.fetch_channel(log_channel_id.log_channel)
        try:
            await log_channel.send(embed)
            await ctx.respond("<a:Right:893842032248885249> Member banned.")  
            return

        except hikari.NotFoundError:
            await ctx.respond("<a:Right:893842032248885249> Member banned, but you don't have a log channel use ``/log``.")  
            return

    except hikari.ForbiddenError:
        await ctx.respond("<a:Wrong:893873540846198844> I can't ban a admin user or more high role at me.")

@plugin.command
@lightbulb.set_help("If the user has the same of higher permissions, it will not be possible to softban it.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("target", "Target you will softban.", hikari.Member)
@lightbulb.option("reason", "Reason for the softban.", default="No reason")
@lightbulb.command(name="softban", description="Ban and unban a member just to delete 7 days messages")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_ban(ctx: lightbulb.SlashContext) -> None:
    log_channel_id = await plugin.bot.d.db.try_fetch_record("SELECT log_channel FROM guild WHERE guild_id = ?", ctx.guild_id)

    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)

    embed = (hikari.Embed(
            title="Member Softbanned",
            colour=Color(0xff0000),
            timestamp=dt.datetime.now().astimezone()
    )
    .add_field(name="<:User:893597475867336795> Member", value=f"{ctx.options.target.mention}", inline=True)
    .add_field(name="<:Staff:893660996458147861> Softbanned by", value=f"{ctx.author.mention}", inline=True)
    .add_field(name="<:Invite:893581721721770064> Reason", value=ctx.options.reason)
    .set_thumbnail(ctx.options.target.avatar_url)
    )
    
    try:
        await guild.ban(ctx.options.target, reason=ctx.options.reason, delete_message_days=7)
        await guild.unban(ctx.options.target)
        if log_channel_id.log_channel == 0:
            await ctx.respond("<a:Right:893842032248885249> Member softbanned, but you don't have a log channel use ``/log``.")  
            return
        try:
            log_channel = await plugin.bot.rest.fetch_channel(log_channel_id.log_channel)
            await log_channel.send(embed)
            await ctx.respond("<a:Right:893842032248885249> Member Softbanned.")  
        
        except hikari.NotFoundError:
            await ctx.respond("<a:Right:893842032248885249> Member softbanned, but you don't have a log channel use ``/log``.")  
            return
    
    except hikari.ForbiddenError:
        await ctx.respond("<a:Wrong:893873540846198844> I can't softban a admin user or more high role at me.")

@plugin.command
@lightbulb.set_help("You can only unban those who are banned")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option("target", "Target you will unban", hikari.Member)
@lightbulb.option("reason", "Reason for the unban", default="No reason")
@lightbulb.command(name="unban", description="Unban a banned user.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_unban(ctx: lightbulb.SlashContext) -> None:
    log_channel_id = await plugin.bot.d.db.try_fetch_record("SELECT log_channel FROM guild WHERE guild_id = ?", ctx.guild_id)

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

    try:
        await guild.unban(ctx.options.target)
        if log_channel_id.log_channel == 0:
            await ctx.respond("<a:Right:893842032248885249> Member unbanned, but you don't have a log channel use ``/log``.")  
            return
        try:
            log_channel = await plugin.bot.rest.fetch_channel(log_channel_id.log_channel)
            await log_channel.send(embed)
            await ctx.respond("<a:Right:893842032248885249> Member unbanned")
            return 

        except hikari.NotFoundError:
            await ctx.respond("<a:Right:893842032248885249> Member unbanned, but you don't have a log channel use ``/log``.")

    except hikari.NotFoundError:
        await ctx.respond("<a:Wrong:893873540846198844> This member is not banned in the guild.")


@plugin.command
@lightbulb.set_help("Add channel for the modmails to this server")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("channel", "Channel you will set for the modmail", hikari.GuildChannel)
@lightbulb.command(name="modmail", description="Set a channel for modmail.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_modmail(ctx: lightbulb.SlashContext) -> None:
    await plugin.bot.d.db.execute(
        "UPDATE guild SET mod_mail = ? WHERE guild_id = ?", 
        ctx.options.channel.id,
        ctx.guild_id
    )
    channel = await plugin.bot.rest.fetch_channel(ctx.options.channel.id)    
    await ctx.respond(f"{channel.mention} Set like ModMail channel succesfully <a:Right:893842032248885249>")


@plugin.command
@lightbulb.set_help("Add channel for the logs to this server")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option("channel", "Channel you will set for the logs", hikari.GuildChannel)
@lightbulb.command(name="log", description="Set a channel for logs.")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_log_channel(ctx: lightbulb.SlashContext) -> None:
    await plugin.bot.d.db.execute(
        "UPDATE guild SET log_channel = ? WHERE guild_id = ?", 
        ctx.options.channel.id,
        ctx.guild_id
    )
    channel = await plugin.bot.rest.fetch_channel(ctx.options.channel.id)    
    await ctx.respond(f"{channel.mention} Set for log channel succesfully <a:Right:893842032248885249>")


@plugin.command
@lightbulb.set_help("The limit for clear messages is 100 and messages of the last 15 days.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option("limit", "Limit of delete messages", int, default=2)
#@lightbulb.option("user", "The user for delete messages", required=False)
@lightbulb.command(name="clear", aliases=("purge",), description="Clear messages")
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext) -> None:
        limit = ctx.options.limit
        if 0 < limit <= 100:
            if limit == 100:
                limit = limit - 1

            channel = await plugin.bot.rest.fetch_channel(ctx.channel_id)
            message = await ctx.respond(f"<a:Loading:893842133792997406> Deleting messages.")
            messages_ = []
            messages_dont = []

            async for messages in plugin.bot.rest.fetch_messages(channel=channel, before=datetime.now().astimezone()).limit(limit):
                time_between_insertion = datetime.now().astimezone() - messages.created_at
                if time_between_insertion.days > 14:
                    messages_dont.append(messages)
                else:
                    messages_.append(messages)

            if len(messages_dont) > 1:
                    await message.edit(content=f"<a:Wrong:893873540846198844> remember that I can only delete messages 14 days old, {len(messages_dont)} messages will be discarded.")
                    await asyncio.sleep(5)

            if len(messages_) > 1:
                await plugin.bot.rest.delete_messages(ctx.channel_id, messages_)
                if ctx.options.limit == 100:
                    message_over = await ctx.respond(content=f"<a:Right:893842032248885249> {len(messages_)+1} Message(s) deleted.")
                    await asyncio.sleep(5)
                    await message_over.delete()
                    return

                message_send = await ctx.respond(content=f"<a:Right:893842032248885249> {len(messages_)} Message(s) deleted.")
                await asyncio.sleep(5)
                await message_send.delete()
            
            else:
                message_end = await ctx.respond(content=f"<a:Right:893842032248885249> {len(messages_)} Message(s) deleted.")
                await asyncio.sleep(5)
                await message_end.delete()

            
        else:
            await ctx.respond("<a:Wrong:893873540846198844> The number of messages you want to delete is not within the limits.")

@plugin.command
@lightbulb.set_help("Add slowmode to the channel: 1s = 1 second, 1m = 1 minute, 1h = 1 hour. Max 6 hours.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.option("time", "Time to add slowmode")
@lightbulb.command(name="slowmode", aliases=("sm",), description="Add slowmode to the channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_slowmode(ctx: lightbulb.SlashContext) -> None:
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
@lightbulb.set_help("Unlock the channel, everyone can use the channel then.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.command(name="unlock", aliases=("ulck",), description="Unlock to everyone.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_unlock(ctx: lightbulb.SlashContext) -> None:
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
    


@plugin.command
@lightbulb.set_help("Lock the channel, just roles with admin persmissions can use the channel.")
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.command(name="lock", aliases=("lck",), description="Lock the channel for moderation.")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_lock(ctx: lightbulb.SlashContext) -> None:
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
        ),
        deny=(
        Permissions.MANAGE_MESSAGES
        | Permissions.SPEAK
        | Permissions.SEND_MESSAGES
        )
    )    
    await ctx.respond(f"???? channel locked.")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)