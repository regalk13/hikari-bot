import lightbulb
import random


from testbot.bot import Bot



class Fun(lightbulb.Plugin):
    @lightbulb.command(name="hello", aliases=("hi", "hey", "aloha", "hola"))
    async def command_hello(self, ctx: lightbulb.Context) -> None:
        """Give a greeting."""
        greeting = random.choice(("Hello", "HI", "Hey"))
        await ctx.respond(f"{greeting} {ctx.member.mention}!", user_mentions=True)



    @lightbulb.command(name="dice", aliases=("roll",))
    async def command_dice(self, ctx: lightbulb.Context, dice: str) -> None:
        """Play a roll dice."""
        number, highest = (int(term) for term in dice.split("d"))

        if number > 25:
            return await ctx.respond("I can only roll up to 25 dice at one time.")


        rolls = [random.randint(1, highest) for i in range(number)]
        await ctx.respond(" + ".join(str(r) for r in rolls) + f" = {sum(rolls):,}", reply=True, mentions_reply=True)


    @lightbulb.command(name="say")
    async def command_say(self, ctx: lightbulb.Context, *, text: str) -> None:
        print(text)

        await ctx.respond(f"``{text}``")


def load(bot: Bot) -> None:
    bot.add_plugin(Fun())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Fun")