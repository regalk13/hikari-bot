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
        async for m in plugin.bot.rest.fetch_members(guild):
            #if (secs := (now - m.joined_at).seconds) <= TIMEOUT:
            #    logging.info(
            #        f"Member '{m.display_name}' joined while offline, scheduling action "
            #        f"in {TIMEOUT-secs} seconds..."
            #    )
            if not m.is_bot:
                await plugin.bot.d.db.execute(
                    "INSERT OR IGNORE INTO user (user_id, user_name, descrip, cookies) VALUES (?, ?, ?, ?)",
                    m.id,
                    m.username,
                    f"Displaying information for {m.mention}",
                    0
                )        
      #  await plugin.bot.d.db.execute(
      #      "INSERT OR IGNORE INTO cookie (user_id, user_name, cookies) VALUES (?, ?, ?)", 
      #      m.id, 
      #      m.username,
            0
       # )

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)