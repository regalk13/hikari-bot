import lightbulb
import hikari
import datetime as dt
from testbot.bot import Bot
from hikari.colors import Color



class Activity(lightbulb.Plugin):
    def __init__(self, bot: Bot):
        super().__init__(name="Activity")
        self.bot = bot
        

    async def activity_app(self, ctx, _id, name, image):
        member = ctx.member
        guild = await self.bot.rest.fetch_guild(member.guild_id)
        voice_state = guild.get_voice_state(user=member.id)

        if voice_state is None:
            await ctx.respond("You need to be in a voice chat")

        else:
            invite = await self.bot.rest.create_invite(target_application=_id, channel=voice_state.channel_id, target_type=2)
            embed = (hikari.Embed(
                    title=f"{name}.",
                    colour=Color(0xBBFFBE),
                    description=f"Access to the activity by clicking [here.]({invite})",
                    timestamp=dt.datetime.now().astimezone()

            )
            .set_thumbnail(image)
            )

            await ctx.respond(embed)

    @lightbulb.command(name="youtube", aliases=("YT", "yt"))
    async def command_youtube(self, ctx: lightbulb.Context) -> None:
        await self.activity_app(ctx, 755600276941176913, "Youtube", "https://cdn.discordapp.com/attachments/860628329362227251/893273830158639125/youtube.png")

    @lightbulb.command(name="betrayal", aliases=("BT", "bt"))
    async def command_betrayal(self, ctx: lightbulb.Context) -> None:
        await self.activity_app(ctx, 773336526917861400, "Betrayal", "https://cdn.discordapp.com/attachments/860628329362227251/893274116172447775/unnamed.png")


    @lightbulb.command(name="fishing", aliases=("FG", "fg"))
    async def command_fishing(self, ctx: lightbulb.Context) -> None:
        await self.activity_app(ctx, 814288819477020702, "Fishing", "https://cdn.discordapp.com/attachments/860628329362227251/893273467212955708/external-content.duckduckgo.com.jpg")


    @lightbulb.command(name="poker", aliases=("PK", "pk"))
    async def command_poker(self, ctx: lightbulb.Context) -> None:
        await self.activity_app(ctx, 755827207812677713, "Poker", "https://cdn.discordapp.com/attachments/860628329362227251/893272821092986900/external-content.duckduckgo.com.jpg")



    @lightbulb.command(name="chess", aliases=("CH", "ch"))
    async def command_chess(self, ctx: lightbulb.Context) -> None:
        await self.activity_app(ctx, 832012774040141894, "Chess", "https://cdn.discordapp.com/attachments/860628329362227251/893271938439454800/images.png")



def load(bot: Bot) -> None:
    bot.add_plugin(Activity(bot))

def unload(bot: Bot) -> None:
    bot.remove_plugin("Activity")