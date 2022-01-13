from __future__ import annotations
from datetime import date
from multiprocessing.connection import wait

from hikari.colors import Color
import typing as t
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari.guilds import Guild
from lightbulb.commands import message
from lightbulb.decorators import option
from pytz import utc
from aiohttp import ClientSession
from hikari.events.base_events import FailedEventT
from apscheduler.triggers.cron import CronTrigger
import os
import hikari
import lightbulb
import logging
from pathlib import Path
import lavasnek_rs
from base64 import b64decode
import sake
from hikari.api import ActionRowBuilder
from datetime import datetime

import random
import testbot
from testbot.bot import db

async def get_prefix(bot, message):
    prefix = await bot.d.db.try_fetch_record("SELECT prefix FROM guild WHERE guild_id = ?", message.guild_id,)
    return prefix.prefix



with open("./secrets/token") as f:
    token = f.read().strip("\n")

bot = lightbulb.BotApp(
        prefix=get_prefix,
        token=token,
        help_slash_command=True,
        case_insensitive_prefix_commands=True,
        intents=hikari.Intents.ALL,
) 

bot.d._dynamic = Path("./data/dynamic")
bot.d._static = bot.d._dynamic.parent / "static"
bot.load_extensions_from("./testbot/bot/extensions", must_exist=True)
bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None: 
    bot.d.scheduler.start()
    bot.d.session = ClientSession(trust_env=True)
    logging.info("AIOHTTP session started")

    bot.d.db = db.Database(bot.d._dynamic, bot.d._static)
    await bot.d.db.connect()
    bot.d.scheduler.add_job(bot.d.db.commit, CronTrigger(second=0))
    cache = sake.redis.RedisCache(app=bot, address="redis://127.0.0.1")
    await cache.open()
    logging.info("Connected to Redis server")

@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    #self.add_check(self.guild_only)
    stdout_channel = await bot.rest.fetch_channel(887515478304624730)
    #await stdout_channel.send(f"Testing v2.0 now online!") 
    logging.info("BOT READY!!!")

@bot.listen(hikari.StoppingEvent)
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.db.close()
    await bot.d.session.close()
    logging.info("AIOHTTP session closed")
    bot.d.scheduler.shutdown() 
    #await bot.d.stdout_channel.send(f"Testing v is shutting now :(") 


@bot.listen(hikari.DMMessageCreateEvent)
async def on_dm_message_create(event: hikari.DMMessageCreateEvent) -> None:
    if event.message.author.is_bot:
        return

    message = await event.message.respond("<a:Loading:893842133792997406> Loading your information.")    
    guilds = bot.rest.fetch_my_guilds()
    row = bot.rest.build_action_row()
    select_menu = row.add_select_menu("select_guild").set_placeholder("Select The Guild").set_min_values(1).set_max_values(1)
    option_devs = select_menu.add_option("Message to devs", "Message to devs").set_description("This message will be sent to my devs.").add_to_menu()
    async for guild in guilds:
        modmail = await bot.d.db.try_fetch_record("SELECT mod_mail FROM guild WHERE guild_id = ?", guild.id)
        if not modmail.mod_mail == 0:
            async for m in bot.rest.fetch_members(guild.id):
                if not m.is_bot:
                    if m.id == event.message.author.id:
                        option = option_devs.add_option(guild.name, guild.id).set_description(guild.name).add_to_menu()        
        else:
            option = option_devs

    await message.delete()

    response = await event.message.respond(
        f"Hello, welcome to the Saiki ModMail service, you can select between the servers that we share and that have a modmail configured (if you don't see your favorite server tell an admin to use ``/modmail``), also you can always send a message to the devs (better bug reports).",
        component=option.add_to_container()
        )
        
    with bot.stream(hikari.InteractionCreateEvent, 1200).filter(
        # Here we filter out events we don't care about.
        lambda e: (
            # A component interaction is a button interaction.
            isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.message == response
        )
    )as stream:
        async for event in stream:
            if event.interaction.values[0] == "Message to devs":
                await event.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_CREATE,
                    "Write the message will be sent to my devs. (Timeout 2 minutes)")

                wait_info = await bot.wait_for(hikari.DMMessageCreateEvent, timeout=120, predicate=lambda x: x.author.id == event.interaction.user.id)
                await event.interaction.message.respond("<a:Right:893842032248885249> The message has been sent to the developers succesfully.")
                content = wait_info.message.content
                
                r_g = random.randint(1, 255)
                r_b = random.randint(1, 255)
                r_r = random.randint(1, 255)

                embed = (hikari.Embed(
                    description=f"Devs Message from {wait_info.author.mention}",
                    colour=Color.from_rgb(r_g, r_b, r_r),
                    timestamp=datetime.now().astimezone()

                )
                .set_author(name=f"{wait_info.author.username}#{wait_info.author.discriminator}", icon=f"{wait_info.author.avatar_url}")
                .set_thumbnail(wait_info.author.avatar_url)
                .add_field(name="<:ID:893578566296555520> User ID", value=wait_info.author_id, inline=True)
                .add_field(name="<:Members:893581084762185739> Name", value=wait_info.author.username, inline=True)
                .add_field(name="<:Presence:893596200148811776> Message", value=f"``{content}``")
                )
                
                stdout_channel = await bot.rest.fetch_channel(887515478304624730)                
                await stdout_channel.send(embed)

            else:
                await event.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_CREATE,
                    "Write the message will be sent to this server. (Timeout 2 minutes)")
                wait_info = await bot.wait_for(hikari.DMMessageCreateEvent, timeout=120, predicate=lambda x: x.author.id == event.interaction.user.id)
                await event.interaction.message.respond("<a:Right:893842032248885249> The message has been sent to the ModMail channel of this server succesfully.")
                content = wait_info.message.content
                r_g = random.randint(1, 255)
                r_b = random.randint(1, 255)
                r_r = random.randint(1, 255)

                embed = (hikari.Embed(
                    description=f"ModMail from {wait_info.author.mention}",
                    colour=Color.from_rgb(r_g, r_b, r_r),
                    timestamp=datetime.now().astimezone()

                )
                .set_author(name=f"{wait_info.author.username}#{wait_info.author.discriminator}", icon=f"{wait_info.author.avatar_url}")
                .set_thumbnail(wait_info.author.avatar_url)
                .add_field(name="<:ID:893578566296555520> User ID", value=wait_info.author_id, inline=True)
                .add_field(name="<:Members:893581084762185739> Name", value=wait_info.author.username, inline=True)
                .add_field(name="<:Presence:893596200148811776> Message", value=f"``{content}``")
                )
                modmail = await bot.d.db.try_fetch_record("SELECT mod_mail FROM guild WHERE guild_id = ?", event.interaction.values[0])
                stdout_channel = await bot.rest.fetch_channel(modmail.mod_mail)                
                await stdout_channel.send(embed)


@bot.listen(hikari.GuildJoinEvent)
async def on_join_guild(event: hikari.GuildJoinEvent) -> None:
        await bot.d.db.execute(
            "INSERT OR IGNORE INTO guild (guild_id, guild_name, prefix, mod_mail, log_channel) values (?, ? ,?, ?, ?)",
            event.guild.id,
            event.guild.name,
            "-",
            0,
            0
        )


        async for m in bot.rest.fetch_members(event.guild.id):
            #if (secs := (now - m.joined_at).seconds) <= TIMEOUT:
            #    logging.info(
            #        f"Member '{m.display_name}' joined while offline, scheduling action "
            #        f"in {TIMEOUT-secs} seconds..."
            #    )
            if not m.is_bot:
                await bot.d.db.execute(
                    "INSERT OR IGNORE INTO user (user_id, user_name, descrip, cookies) VALUES (?, ?, ?, ?)",
                    m.id,
                    m.username,
                    f"Displaying information for {m.mention}",
                    0
                )        

@bot.listen(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    if not event.member.is_bot:
        await bot.d.db.execute(
                "INSERT OR IGNORE INTO user (user_id, user_name, descrip, cookies) VALUES (?, ?, ?, ?)",
                event.member.id,
                event.member.username,
                f"Displaying information for {event.member.mention}",
                0
            )
        return


@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[FailedEventT]) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return None

    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("<a:Warn:893874049967595550> Some arguments are missing: "+ ", ".join(event.exception.missing_options))
        
    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("<a:Warn:893874049967595550> Too many arguments were passed.")

    if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        return await event.context.respond(f"<a:Warn:893874049967595550> Command is on cooldown. Try again in {event.exception.retry_after:.0f} second(s).")

    if isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
        return await event.context.respond("<a:Wrong:893873540846198844> You don't have the required permissions for this action.")

    if isinstance(event.exception, lightbulb.errors.BotMissingRequiredPermission):
        return await event.context.respond("<a:Wrong:893873540846198844> I don't have the required permissions for this action.")

    if isinstance(event.exception.__cause__, hikari.ForbiddenError):
        await event.context.respond("<a:Wrong:893873540846198844> Something is missing perms or missed ids.")
        raise event.exception

    if isinstance(event.exception, lightbulb.errors.CheckFailure):
        return None

    await event.context.respond("An error has occurred <:tiste:889343933304426536>, it can be caused by the following:\n - The command is broken.\n - The command is under maintenance.\n - You don't use the command correctly look at its help.")
    raise event.exception


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name=f"/help • Version 0.2.3",
            type=hikari.ActivityType.WATCHING,
        )
    )