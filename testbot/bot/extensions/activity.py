import lightbulb
import hikari
import datetime as dt

from hikari.colors import Color

plugin = lightbulb.Plugin(name="Activity", description="Create and join in game activities of Discord Game Labs.")
#at the moment discord does not allow to enable them in all severs we will see what could happen
#773336526917861400 - betrayal
#755827207812677713 - Poker 
#832012774040141894 - chess 
#879863686565621790 - letter 
#879863976006127627 - worksnak
#878067389634314250 - doodlecrew

async def activity_app(ctx, _id, name, image):
    member = ctx.member
    guild = await plugin.bot.rest.fetch_guild(member.guild_id)
    voice_state = guild.get_voice_state(user=member.id)

    if voice_state is None:
        await ctx.respond("You need to be in a voice chat")

    else:
        invite = await plugin.bot.rest.create_invite(target_application=_id, channel=voice_state.channel_id, target_type=2)
        embed = (hikari.Embed(
                title=f"{name}",
                colour=Color(0xBBFFBE),
                description=f"Access to the activity by clicking [here.]({invite})",
                timestamp=dt.datetime.now().astimezone()

        )
        .set_thumbnail(image)
        )

        await ctx.respond(embed, reply=True)


# @plugin.command
# @lightbulb.set_help("Create link of join, remember to be in a vc and you can watch youtube with your friends")
# @lightbulb.command(name="youtube", aliases=("YT", "yt"), description="Watch videos of youtube")
# @lightbulb.implements(lightbulb.PrefixCommand)
# async def command_youtube(ctx: lightbulb.Context,) -> None:
#    await activity_app(ctx, 755600276941176913, "Youtube", "https://cdn.discordapp.com/attachments/860628329362227251/893273830158639125/youtube.png")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)