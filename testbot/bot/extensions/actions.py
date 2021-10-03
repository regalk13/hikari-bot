import lightbulb
import hikari
import requests
from hikari.colors import Color
import random
import json
from testbot.bot import Bot



class Actions(lightbulb.Plugin):


    def get_gif(self, term) -> str:
        api_key = "36SW53ZHFSNF"
        limit = 14
    
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (term, api_key, limit))


        gifs_data = json.loads(r.content)
        gif = gifs_data["results"][random.randint(0,13)]["media"][0]["gif"]["url"]

        return gif

    async def action(self, ctx: lightbulb.Context, text, image) -> None:
        r_g = random.randint(1, 255)
        r_b = random.randint(1, 255)
        r_r = random.randint(1, 255)

        embed = (hikari.Embed(
            description=f"{text}",
            colour=Color.from_rgb(r_g, r_b, r_r)
        )
        .set_image(image)
        )

        await ctx.respond(embed)


    @lightbulb.command(name="kiss", aliases=("Kiss",))
    async def command_kiss(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kiss")
        await self.action(ctx, f"**{ctx.member.username}** le dio un beso a **{target.username}**. (づ￣ ³￣)づ", gif)


    @lightbulb.command(name="angry", aliases=("Angry",))
    async def command_angry(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-angry")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** got mad >:C", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** got mad with **{target.username}**", gif)


    @lightbulb.command(name="claps", aliases=("Claps",))
    async def command_clap(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-clap")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is clapping.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** applauds **{target.username}**", gif)


    @lightbulb.command(name="highfive", aliases=("Highfive",))
    async def command_highfive(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-highfive")

        if target == None:
            await self.action(ctx, f"Highfive!!!", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** highfive to **{target.username}**", gif)


    @lightbulb.command(name="laugh", aliases=("Laugh",))
    async def command_laugh(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-laugh")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is laughing.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** laughs at **{target.username}**", gif)


    @lightbulb.command(name="scare", aliases=("Scare",))
    async def command_scare(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-scare")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is scared.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** scared by **{target.username}**", gif)


    @lightbulb.command(name="splash", aliases=("Splash",))
    async def command_splash(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-splash")
        await self.action(ctx, f"**{ctx.member.username}** splash to **{target.username}**", gif)


    @lightbulb.command(name="tsundere", aliases=("Tsundere",))
    async def command_tsundere(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-tsundere")

        if target == None:
            await self.action(ctx, f"¬¬ ¡Hmm! silly **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is being tsundere with **{target.username}**", gif)


    @lightbulb.command(name="baka", aliases=("Baka",))
    async def command_baka(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-baka")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** BAKA!!!", gif)

        else:
            await self.action(ctx, f"**{target.username}** BAKA!!!", gif)


    @lightbulb.command(name="cook", aliases=("Cook",))
    async def command_cook(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-cook")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is cooking something delicious.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is cooking something delicious for **{target.username}**", gif)

    
    @lightbulb.command(name="handholding", aliases=("Handholding",))
    async def command_handholding(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-handholding")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** take my hand.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** hand holding with **{target.username}**", gif)



    @lightbulb.command(name="hug", aliases=("Hug",))
    async def command_hug(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-hug")
        await self.action(ctx, f"**{ctx.member.username}** hug to **{target.username}**", gif)

    
    @lightbulb.command(name="lick", aliases=("Lick",))
    async def command_lick(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-lick")
        await self.action(ctx, f"**{ctx.member.username}** lick to **{target.username}**", gif)


    @lightbulb.command(name="shoot", aliases=("Shoot",))
    async def command_shoot(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-shoot")

        if target == None:
            await self.action(ctx, f"**Saiki** shoot to **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** shoot to **{target.username}**", gif)


    @lightbulb.command(name="spray", aliases=("Spray",))
    async def command_spray(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-spray")

        if target == None:
            await self.action(ctx, f"**Saiki** spray to **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** spray to **{target.username}**", gif)


    @lightbulb.command(name="bite", aliases=("Bite",))
    async def command_bite(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-bite")

        await self.action(ctx, f"**{ctx.member.username}** bit **{target.username}**", gif)

    @lightbulb.command(name="cuddle", aliases=("Cuddle",))
    async def command_cuddle(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-cuddle")

        await self.action(ctx, f"**{ctx.member.username}** cuddled with **{target.username}**", gif)


    @lightbulb.command(name="heal", aliases=("Heal",))
    async def command_heal(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-heal")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is healing", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is healing to **{target.username}**", gif)
    

    @lightbulb.command(name="kickbutt", aliases=("Kickbutt",))
    async def command_kickbutt(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kickbutt")

        await self.action(ctx, f"**{ctx.member.username}** kick butt to **{target.username}**", gif)


    @lightbulb.command(name="pat", aliases=("Pat",))
    async def command_pat(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-pat")

        await self.action(ctx, f"**{ctx.member.username}** pat to **{target.username}**", gif)

    @lightbulb.command(name="slap", aliases=("Slap",))
    async def command_slap(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-slap")

        await self.action(ctx, f"**{ctx.member.username}** slapped to **{target.username}**", gif)

    @lightbulb.command(name="stare", aliases=("Stare",))
    async def command_stare(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-stare")

        if target == None:
            await self.action(ctx, f"o.o stare **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** stare to **{target.username}**", gif)

    @lightbulb.command(name="bye", aliases=("Bye",))
    async def command_bye(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-bye")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** say bye", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** say bye to **{target.username}**", gif)

    @lightbulb.command(name="feed", aliases=("Feed",))
    async def command_feed(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-feed")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** yummy :3", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** feeds **{target.username}**", gif)

    @lightbulb.command(name="hi", aliases=("Hi",))
    async def command_hi(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-hi")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** say hi", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** say hi to **{target.username}**", gif)
    
    @lightbulb.command(name="kill", aliases=("Kill",))
    async def command_kill(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kill")

        await self.action(ctx, f"**{ctx.member.username}** killed **{target.username}**", gif)


    @lightbulb.command(name="poke", aliases=("Poke",))
    async def command_poke(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-poke")

        await self.action(ctx, f"**{ctx.member.username}** bothers to **{target.username}**", gif)

    @lightbulb.command(name="snowball", aliases=("Snowball",))
    async def command_snowball(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-snowball")

        await self.action(ctx, f"**{ctx.member.username}** I throw a snowball at **{target.username}**", gif)

    

def load(bot: Bot) -> None:
    bot.add_plugin(Actions())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Actions")