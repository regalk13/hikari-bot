import datetime as dt
import logging

import hikari
import lightbulb

TIMEOUT = 600

plugin = lightbulb.Plugin("Gateway")


@plugin.listener(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    now = dt.datetime.now().astimezone()

    guilds = plugin.bot.rest.fetch_my_guilds()

    async for guild in guilds:

        await plugin.bot.d.db.execute(
            "INSERT OR IGNORE INTO guild (guild_id, guild_name, prefix, mod_mail, log_channel) values (?, ? ,?, ?, ?)",
            guild.id,
            guild.name,
            "-",
            0,
            0
        )
        async for m in plugin.bot.rest.fetch_members(guild):
            if not m.is_bot:
                await plugin.bot.d.db.execute(
                    "INSERT OR IGNORE INTO user (user_id, user_name, descrip, cookies) VALUES (?, ?, ?, ?)",
                    m.id,
                    m.username,
                    f"Displaying information for {m.mention}",
                    0
                )        

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)