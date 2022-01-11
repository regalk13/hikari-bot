import hikari
import lightbulb
import aiofiles
import asyncio
import os
from aiohttp import client_exceptions


from hashlib import md5
from virus_total_apis import PublicApi

plugin = lightbulb.Plugin(name="Virus", description="Scan files and urls for any type of virus")

with open("./secrets/api-virus", "r") as f:
    API_KEY = f.readline()

api = PublicApi(API_KEY)

@plugin.command()
@lightbulb.set_help("Scan whatever file for virus (the upload and results it may take a time)")
@lightbulb.command(name="scan", description="Scan files for virus")
@lightbulb.implements(lightbulb.PrefixCommand)
async def cmd_scan_file(ctx: lightbulb.PrefixContext):
    attachment = ctx.attachments[0]
    
    message = await ctx.respond("<a:Loading:893842133792997406> Getting the file...")
    async with aiofiles.open(f"./files/{attachment.filename}", "wb") as fp:
        async with attachment.stream() as stream:
            async for chunk in stream:
                await fp.write(chunk)

    await message.edit("<a:Loading:893842133792997406> Sending file to virustotal server...")

    with open(f"./files/{attachment.filename}", "rb") as f:
        file_hash = md5(f.read()).hexdigest()
    
    response = api.get_file_report(file_hash)

    
    await message.edit("<a:Loading:893842133792997406> checking if it is in the data already scanned or it will be scanned.")

    embed = (hikari.Embed(
        title="File-Scan Results",
        color=0x5deb1f
    ))

    embed_ = (hikari.Embed(
        title="File-Scan Results",
        color=0xfa2617
    ))

    try:
        if response["response_code"] == 200:
            if response["results"]["positives"] > 0:
                link = response["results"]["permalink"]
                embed_.add_field(name="Malicious file.", value=f"The scanner has detected this is a malicious file [click]({link}).")
                await message.delete()
                await ctx.respond(embed_)
            else:
                link = response["results"]["permalink"]
                embed.add_field(name="Safe file.", value=f"The scanner has detected this is a safe file [click]({link}).")
                await message.delete()
                await ctx.respond(embed)
        else:
            await ctx.respond("Could not get the analysis of the file.")

    except KeyError:
        
        response = api.scan_file(f"./files/{attachment.filename}")

        if response["response_code"] == 200:
            link = response["results"]["permalink"]
            print(response["results"]["permalink"])
            embed.add_field(name="Scanned.", value=f"This file was not in the database and therefore it was analyzed for the first time [click]({link}).")
            await message.delete()
            await ctx.respond(embed)

        else:
            await ctx.respond("Could not get the analysis of the file.")
        

    await asyncio.sleep(10)
    os.remove(f"./files/{attachment.filename}")


@plugin.command()
@lightbulb.set_help("Scan whatever url for virus (the upload and results it may take a time)")
@lightbulb.option("url", "The url to scan")
@lightbulb.command(name="scanu", description="Scan urls for virus")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_scan_file(ctx: lightbulb.SlashContext):
    
    message = await ctx.respond("<a:Loading:893842133792997406> scanning the url...", reply=True)
    url = ctx.options.url
    try:
        async with ctx.bot.d.session.get(url) as r:
                if not r.ok:
                    await ctx.respond("Not valid url")
                    return
    except client_exceptions.InvalidURL:
        await message.edit("<a:Wrong:893873540846198844> Not valid url")
        return
    
    await message.edit("<a:Loading:893842133792997406> checking if the url has already been analyzed.")

    embed = (hikari.Embed(
        title="Url-Scan Results",
        color=0x5deb1f
    ))

    embed_ = (hikari.Embed(
        title="Url-Scan Results",
        color=0xfa2617
    ))

    response = api.get_url_report(url)
    print(response)
    try:
        if response["response_code"] == 200:
            if response["results"]["positives"] > 0:
                link = response["results"]["permalink"]
                embed_.add_field(name="Malicious site.", value=f"The scanner has detected that this site as malicious [click]({link}).")
                await message.delete()
                await ctx.respond(embed_)
            else:
                link = response["results"]["permalink"]
                embed.add_field(name="Safe site.", value=f"The scanner has detected that this is site as safe [click]({link}).")
                await message.delete()
                await ctx.respond(embed)
        else:
            await ctx.respond("Could not get the analysis of the site.")

    except KeyError:
        
        response = api.scan_url(url)

        if response["response_code"] == 200:
            link = response["results"]["permalink"]
            print(response["results"]["permalink"])
            embed.add_field(name="Scanned.", value=f"This site was not in the database and therefore it was analyzed for the first time [click]({link}).")
            await message.delete()
            await ctx.respond(embed)

        else:
            await ctx.respond("Could not get the analysis of the site.")
        
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)