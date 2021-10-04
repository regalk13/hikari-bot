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

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="kiss", aliases=("Kiss",))
    async def command_kiss(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kiss")
        await self.action(ctx, f"**{ctx.member.username}** le dio un beso a **{target.username}**. (づ￣ ³￣)づ", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="angry", aliases=("Angry",))
    async def command_angry(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-angry")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** got mad >:C", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** got mad with **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="claps", aliases=("Claps",))
    async def command_clap(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-clap")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is clapping.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** applauds **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="highfive", aliases=("Highfive",))
    async def command_highfive(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-highfive")

        if target == None:
            await self.action(ctx, f"Highfive!!!", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** highfive to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="laugh", aliases=("Laugh",))
    async def command_laugh(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-laugh")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is laughing.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** laughs at **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="scare", aliases=("Scare",))
    async def command_scare(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-scare")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is scared.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** scared by **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="splash", aliases=("Splash",))
    async def command_splash(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-splash")
        await self.action(ctx, f"**{ctx.member.username}** splash to **{target.username}**", gif)


    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="tsundere", aliases=("Tsundere",))
    async def command_tsundere(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-tsundere")

        if target == None:
            await self.action(ctx, f"¬¬ ¡Hmm! silly **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is being tsundere with **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="baka", aliases=("Baka",))
    async def command_baka(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-baka")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** BAKA!!!", gif)

        else:
            await self.action(ctx, f"**{target.username}** BAKA!!!", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="cook", aliases=("Cook",))
    async def command_cook(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-cook")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is cooking something delicious.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is cooking something delicious for **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)    
    @lightbulb.command(name="handholding", aliases=("Handholding",))
    async def command_handholding(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-handholding")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** take my hand.", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** hand holding with **{target.username}**", gif)


    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="hug", aliases=("Hug",))
    async def command_hug(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-hug")
        await self.action(ctx, f"**{ctx.member.username}** hug to **{target.username}**", gif)

    
    @lightbulb.command(name="lick", aliases=("Lick",))
    async def command_lick(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-lick")
        await self.action(ctx, f"**{ctx.member.username}** lick to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="shoot", aliases=("Shoot",))
    async def command_shoot(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-shoot")

        if target == None:
            await self.action(ctx, f"**Saiki** shoot to **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** shoot to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="spray", aliases=("Spray",))
    async def command_spray(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-spray")

        if target == None:
            await self.action(ctx, f"**Saiki** spray to **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** spray to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="bite", aliases=("Bite",))
    async def command_bite(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-bite")

        await self.action(ctx, f"**{ctx.member.username}** bit **{target.username}**", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="cuddle", aliases=("Cuddle",))
    async def command_cuddle(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-cuddle")

        await self.action(ctx, f"**{ctx.member.username}** cuddled with **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="heal", aliases=("Heal",))
    async def command_heal(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-heal")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is healing", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is healing to **{target.username}**", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="kickbutt", aliases=("Kickbutt",))
    async def command_kickbutt(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kickbutt")

        await self.action(ctx, f"**{ctx.member.username}** kick butt to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="pat", aliases=("Pat",))
    async def command_pat(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-pat")

        await self.action(ctx, f"**{ctx.member.username}** pat to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="slap", aliases=("Slap",))
    async def command_slap(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-slap")

        await self.action(ctx, f"**{ctx.member.username}** slapped to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="stare", aliases=("Stare",))
    async def command_stare(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-stare")

        if target == None:
            await self.action(ctx, f"o.o stare **{ctx.member.username}**", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** stare to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="bye", aliases=("Bye",))
    async def command_bye(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-bye")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** say bye", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** say bye to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="feed", aliases=("Feed",))
    async def command_feed(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-feed")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** yummy :3", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** feeds **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="hi", aliases=("Hi",))
    async def command_hi(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-hi")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** say hi", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** say hi to **{target.username}**", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)    
    @lightbulb.command(name="kill", aliases=("Kill",))
    async def command_kill(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-kill")

        await self.action(ctx, f"**{ctx.member.username}** killed **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="poke", aliases=("Poke",))
    async def command_poke(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-poke")

        await self.action(ctx, f"**{ctx.member.username}** bothers to **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="snowball", aliases=("Snowball",))
    async def command_snowball(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-snowball")

        await self.action(ctx, f"**{ctx.member.username}** I throw a snowball at **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="tickle", aliases=("Tickle",))
    async def command_tickle(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-tickle")

        if target == None:
            await self.action(ctx, f"Jejeje :D", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** tickles **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="cheeks", aliases=("Cheeks",))
    async def command_cheeks(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-cheeks")

        if target == None:
            await self.action(ctx, f"Jejeje :D", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** pin the cheeks of**{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="gaming", aliases=("Gaming",))
    async def command_gaming(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-gaming")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is playing", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is playing with **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="punch", aliases=("Punch",))
    async def command_punch(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-punch")

        await self.action(ctx, f"**{ctx.member.username}** punch **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="spank", aliases=("Spank",))
    async def command_spank(self, ctx: lightbulb.Context, target: lightbulb.member_converter) -> None:
        gif = self.get_gif("anime-spank")

        await self.action(ctx, f"**{ctx.member.username}** spank **{target.username}**", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="sleep", aliases=("Sleep",))
    async def command_sleep(self, ctx: lightbulb.Context, target: lightbulb.member_converter = None) -> None:
        gif = self.get_gif("anime-sleep")

        if target == None:
            await self.action(ctx, f"**{ctx.member.username}** is sleeping or going to sleep", gif)

        else:
            await self.action(ctx, f"**{ctx.member.username}** is sleeping or going to sleep whit **{target.username}**", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="confused", aliases=("Confused",))
    async def command_confused(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-confused")

        await self.action(ctx, f"**{ctx.member.username}** is confused.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="disgusted", aliases=("Disgusted",))
    async def command_disgusted(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-disgusted")

        await self.action(ctx, f"**{ctx.member.username}** is disgusted.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="happy", aliases=("Happy",))
    async def command_happy(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-happy")

        await self.action(ctx, f"**{ctx.member.username}** feels happy.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="pout", aliases=("Pout",))
    async def command_disgusted(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-pout")

        await self.action(ctx, f"**{ctx.member.username}** pouts.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="shrug", aliases=("Shrug",))
    async def command_shrug(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-shrug")

        await self.action(ctx, f"**{ctx.member.username}** doesn't know or doesn't care.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="teehee", aliases=("Teehee",))
    async def command_teehee(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-teehee")

        await self.action(ctx, f"**{ctx.member.username}** giggles. >w<", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="wasted", aliases=("Wasted",))
    async def command_wasted(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-wasted")

        await self.action(ctx, f"**{ctx.member.username}** wasted...", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="banghead", aliases=("Banghead",))
    async def command_banghead(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-banghead")

        await self.action(ctx, f"**{ctx.member.username}** hits his head.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="cry", aliases=("Cry",))
    async def command_cry(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-cry")

        await self.action(ctx, f"**{ctx.member.username}** is crying.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="drunk", aliases=("Drunk",))
    async def command_drunk(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-drunk")

        await self.action(ctx, f"**{ctx.member.username}** got drunk.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="lewd", aliases=("Lewd",))
    async def command_lewd(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-lewd")

        await self.action(ctx, f"**{ctx.member.username}** is thinking lewd things.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="psycho", aliases=("Psycho",))
    async def command_psycho(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-psycho")

        await self.action(ctx, f"**{ctx.member.username}** psycho mode.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="sing", aliases=("Sing",))
    async def command_sing(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-sing")

        await self.action(ctx, f"**{ctx.member.username}** is singing.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="think", aliases=("Think",))
    async def command_think(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-think")

        await self.action(ctx, f"**{ctx.member.username}** is thinking.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="yandere", aliases=("Yandere",))
    async def command_yandere(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-yandere")

        await self.action(ctx, f"**{ctx.member.username}** yandere mode.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="blush", aliases=("Blush",))
    async def command_blush(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-blush")

        await self.action(ctx, f"**{ctx.member.username}** blushed.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="eat", aliases=("Eat",))
    async def command_eat(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-eat")

        await self.action(ctx, f"**{ctx.member.username}** is eating.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="like", aliases=("Like",))
    async def command_like(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-likes")

        await self.action(ctx, f"**{ctx.member.username}** likes it.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="run", aliases=("Run",))
    async def command_run(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-run")

        await self.action(ctx, f"**{ctx.member.username}** is running.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="sip", aliases=("Sip",))
    async def command_run(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-sip")

        await self.action(ctx, f"**{ctx.member.username}** sips.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="run", aliases=("Run",))
    async def command_run(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-run")

        await self.action(ctx, f"**{ctx.member.username}** is running.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="boom", aliases=("Boom",))
    async def command_boom(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-explosion")

        await self.action(ctx, f"Boom!!!.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="dance", aliases=("Dance",))
    async def command_dance(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-dance")

        await self.action(ctx, f"**{ctx.member.username}** is dancing.", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="facepalm", aliases=("Facepalm",))
    async def command_facepalm(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-facepalm")

        await self.action(ctx, f"**{ctx.member.username}** face palm.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="nope", aliases=("Nope",))
    async def command_nope(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-nope")

        await self.action(ctx, f"**{ctx.member.username}** say nope.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="sad", aliases=("Sad",))
    async def command_sad(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-sad")

        await self.action(ctx, f"**{ctx.member.username}** feels sad man.", gif)
            
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="wag", aliases=("Wag",))
    async def command_wag(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-wag-tail")

        await self.action(ctx, f"**{ctx.member.username}** wag his tail.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="vomit", aliases=("Vomit",))
    async def command_vomit(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-vomit")

        await self.action(ctx, f"**{ctx.member.username}** is vomiting.", gif)
            
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="bored", aliases=("Bored",))
    async def command_bored(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-bored")

        await self.action(ctx, f"**{ctx.member.username}** is bored.", gif)

    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="deredere", aliases=("Deredere",))
    async def command_deredere(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-deredere")

        await self.action(ctx, f"**{ctx.member.username}** falls in love.", gif)
   
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="fail", aliases=("Fail",))
    async def command_fail(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-fail")

        await self.action(ctx, f"**{ctx.member.username}** failed.", gif)
   
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="peek", aliases=("Peek",))
    async def command_peek(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-peek")

        await self.action(ctx, f"**{ctx.member.username}** is peeking", gif)
    
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="scream", aliases=("Scream",))
    async def command_scream(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-scream")

        await self.action(ctx, f"**{ctx.member.username}** scream!!!", gif)
   
    @lightbulb.cooldown(4, 3, lightbulb.UserBucket)
    @lightbulb.command(name="smug", aliases=("Smug",))
    async def command_smug(self, ctx: lightbulb.Context) -> None:
        gif = self.get_gif("anime-smug")

        await self.action(ctx, f"**{ctx.member.username}** smuging.", gif)


    

def load(bot: Bot) -> None:
    bot.add_plugin(Actions())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Actions")