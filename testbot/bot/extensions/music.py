import logging
from typing import Optional
import hikari
from hikari.api import voice
import lightbulb
import lavasnek_rs
import random
from hikari.colors import Color
from hikari.messages import ButtonStyle

HIKARI_VOICE = False

class EventHandler:
    """Events from the Lavalink server"""
    async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        node = await plugin.bot.d.lavalink.get_guild_node(event.guild_id)
        await now_playing_event(node, event)
        logging.info("Track started on guild: %s", event.guild_id)

    async def track_finish(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        logging.info("Track finished on guild: %s", event.guild_id)

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning("Track exception event happened on guild: %d", event.guild_id)

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)


plugin = lightbulb.Plugin(name="Music", description="Music commands for your bot.")

async def now_playing_event(node, event_):
    components = []    
    componentens_ = plugin.bot.rest.build_action_row() 
    button_pause = componentens_.add_button(ButtonStyle.PRIMARY, "but_pause").set_label("Pause").add_to_container()
    button_skip = componentens_.add_button(ButtonStyle.DANGER, "but_skip").set_label("Skip").add_to_container()
    button_stop = componentens_.add_button(ButtonStyle.PRIMARY, "but_stop").set_label("Stop").add_to_container()

    components.append(componentens_)

    channel = await node.get_data()
    stdout_channel = plugin.bot.cache.get_guild_channel(channel)
    response = await stdout_channel.send(
        hikari.Embed(
        description=f"Now Playing: **{node.now_playing.track.info.title}**",
        color=0x5deb1f
        ),
        components=components,
    )
    with plugin.bot.stream(hikari.InteractionCreateEvent, 1200).filter(
        # Here we filter out events we don't care about.
        lambda e: (
            # A component interaction is a button interaction.
            isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.message == response
        )
    )as stream:
        async for event in stream:
            user = event.interaction.user
            states = plugin.bot.cache.get_voice_states_view_for_guild(event_.guild_id)
            voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == user.id)]
            
            try:
                if voice_state[0].channel_id == voice_state[1].channel_id:
                    # If we made it through the filter, the user has clicked
                    # one of our buttons, so we grab the custom ID.
                    cid = event.interaction.custom_id

                    embed_paused=(hikari.Embed(
                    description=f"Paused: **{node.now_playing.track.info.title}**",
                    color=0x5deb1f
                    ))


                    embed_skiped=(hikari.Embed(
                    description=f"Skipped: **{node.now_playing.track.info.title}**",
                    color=0x5deb1f
                    ))

                    embed_stop=(hikari.Embed(
                    title=f"Stopped: {node.now_playing.track.info.title}",
                    description=f"Press ``Skip`` to close the player.",
                    color=0xfa2617
                    ))

                    embed_resumed=(hikari.Embed(
                    description=f"Now playing: **{node.now_playing.track.info.title}**",
                    color=0x5deb1f
                    ))
                    
                    if cid == "but_pause":
                        try:
                            components_ = []
                            componentens = plugin.bot.rest.build_action_row() 
                            button_resume = componentens.add_button(ButtonStyle.PRIMARY, "but_resume").set_label("Resume").add_to_container()
                            button_skip = componentens.add_button(ButtonStyle.DANGER, "but_skip").set_label("Skip").add_to_container()
                            button_stop = componentens.add_button(ButtonStyle.PRIMARY, "but_stop").set_label("Stop").add_to_container()

                            components_.append(componentens)


                            await event.interaction.create_initial_response(
                                hikari.ResponseType.MESSAGE_UPDATE,
                                embed=embed_paused,
                                components=components_
                            )
                            await plugin.bot.d.lavalink.pause(event_.guild_id)

                        except hikari.NotFoundError:
                            await event.interaction.edit_initial_response(
                                embed=embed_paused,
                            )

                    elif cid == "but_skip":
                        try:
                            await event.interaction.create_initial_response(
                                hikari.ResponseType.MESSAGE_UPDATE,
                                embed=embed_skiped,
                            )
                            
                            skip = await plugin.bot.d.lavalink.skip(event_.guild_id)
                            node = await plugin.bot.d.lavalink.get_guild_node(event_.guild_id)

                            if not skip:
                                print("Nothing to skip")
                            else:
                            # If the queue is empty, the next track won't start playing (because there isn't any),
                            # so we stop the player.
                                if not node.queue and not node.now_playing:
                                    await plugin.bot.d.lavalink.stop(event_.guild_id)
                                
                                await response.delete()

                        except hikari.NotFoundError:
                            await event.interaction.edit_initial_response(
                                embed=embed_skiped,
                            )

                    elif cid == "but_stop":
                        try:
                            await event.interaction.create_initial_response(
                                hikari.ResponseType.MESSAGE_UPDATE,
                                embed=embed_stop,
                            )

                            await plugin.bot.d.lavalink.stop(event_.guild_id)
                            
                        except:   
                            await event.interaction.edit_initial_response(
                                embed=embed_stop,
                            )


                    elif cid == "but_resume":
                        try:
                            await event.interaction.create_initial_response(
                                hikari.ResponseType.MESSAGE_UPDATE,
                                embed=embed_resumed,
                                components=components
                            )
                            
                            
                            await plugin.bot.d.lavalink.resume(event_.guild_id)

                        except:   
                            await event.interaction.edit_initial_response(
                                embed=embed_stop,
                            )

                else:
                    await event.interaction.create_initial_response(
                        hikari.ResponseType.MESSAGE_CREATE,
                        "You need to be on the same voice chat as saiki.",
                        flags=hikari.MessageFlag.EPHEMERAL
                    )

            except IndexError:
                    await event.interaction.create_initial_response(
                        hikari.ResponseType.MESSAGE_CREATE,
                        "You need to be on the same voice chat as saiki.",
                        flags=hikari.MessageFlag.EPHEMERAL
                    )


async def _join(ctx: lightbulb.Context) -> Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.member.id)]
    bot_voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727)]

    if not voice_state:
        await ctx.respond("Connect to a voice channel first.")
        return None

    if bot_voice_state:
        await ctx.respond("I'm already on a voice channel")
        return

    channel_id = voice_state[0].channel_id

    if HIKARI_VOICE:
        assert ctx.guild_id is not None

        await plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
        connection_info = await plugin.bot.d.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    else:
        try:
            connection_info = await plugin.bot.d.lavalink.join(ctx.guild_id, channel_id)
        except TimeoutError:
            await ctx.respond(
                "I was unable to connect to the voice channel, maybe missing permissions? or some internal issue."
            )
            return None

    await plugin.bot.d.lavalink.create_session(connection_info)

    return channel_id

@plugin.listener(hikari.ShardReadyEvent)
async def start_lavalink(event: hikari.ShardReadyEvent) -> None:
    """Event that triggers when the hikari gateway is ready."""
    with open("./secrets/token") as f:
        token = f.read().strip("\n")
    builder = (
        # TOKEN can be an empty string if you don't want to use lavasnek's discord gateway.
        lavasnek_rs.LavalinkBuilder(event.my_user.id, token)
        # This is the default value, so this is redundant, but it's here to show how to set a custom one.
        .set_host("127.0.0.1").set_password('PASSWORD_ADMIN')
    )

    if HIKARI_VOICE:
        builder.set_start_gateway(False)

    lava_client = await builder.build(EventHandler())

    plugin.bot.d.lavalink = lava_client

@plugin.command()
@lightbulb.command("join", "Joins the voice channel you are in.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def join(ctx: lightbulb.SlashContext) -> None:
    """Joins the voice channel you are in."""
    channel_id = await _join(ctx)

    embed = (hikari.Embed(
        description=f"**Joined** <#{channel_id}>",
        color=0x5deb1f
    ))

    if channel_id:
        await ctx.respond(embed)


@plugin.command()
@lightbulb.command("leave", "Leaves the voice channel the bot is in, clearing the queue.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def leave(ctx: lightbulb.SlashContext) -> None:
    """Leaves the voice channel the bot is in, clearing the queue."""

    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return



    await plugin.bot.d.lavalink.destroy(ctx.guild_id)

    if HIKARI_VOICE:
        if ctx.guild_id is not None:
            await plugin.bot.update_voice_state(ctx.guild_id, None)
            await plugin.bot.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    else:
        await plugin.bot.d.lavalink.leave(ctx.guild_id)

    # Destroy nor leave remove the node nor the queue loop, you should do this manually.
    await plugin.bot.d.lavalink.remove_guild_node(ctx.guild_id)
    await plugin.bot.d .lavalink.remove_guild_from_loops(ctx.guild_id)


    embed = (hikari.Embed(
        title="Left voice channel",
        description="I left the channel correctly.",
        color=0x5deb1f
    )
    )

    await ctx.respond(embed)


@plugin.command()
@lightbulb.option("query", "The query to search for.", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("play", "Searches the query on youtube, or adds the URL to the queue.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def play(ctx: lightbulb.SlashContext) -> None:
    """Searches the query on youtube, or adds the URL to the queue."""
    
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return


    query = ctx.options.query

    if not query:
        await ctx.respond("Please specify a query.")
        return None

    con = plugin.bot.d.lavalink.get_guild_gateway_connection_info(ctx.guild_id)
    # Join the user's voice channel if the bot is not in one.
    if not con:
        await _join(ctx)

    # Search the query, auto_search will get the track from a url if possible, otherwise,
    # it will search the query on youtube.
    query_information = await plugin.bot.d.lavalink.auto_search_tracks(query)

    if not query_information.tracks:  # tracks is empty    
        await ctx.respond("<a:Wrong:893873540846198844> Could not find any video of the search query.")
        return

    try:
        # `.requester()` To set who requested the track, so you can show it on now-playing or queue.
        # `.queue()` To add the track to the queue rather than starting to play the track now.
        await plugin.bot.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)
        await node.set_data(ctx.channel_id)
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond(f"Use `/join` first")
        return

    embed = (hikari.Embed(
        description=f"Added to queue: **{query_information.tracks[0].info.title}**",
        color=0x5deb1f
    ))

    await ctx.respond(embed)


@plugin.command()
@lightbulb.command("stop", "Stops the current song (skip to continue).")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stop(ctx: lightbulb.SlashContext) -> None:
    """Stops the current song (skip to continue)."""

    
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    await plugin.bot.d.lavalink.stop(ctx.guild_id)

    embed = (hikari.Embed(
        title="Stopped playing",
        description="You can use /skip to continue playing songs.",
        colour=0xfa2617
    )
    )

    await ctx.respond(embed)


@plugin.command()
@lightbulb.command("skip", "Skips the current song.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skip(ctx: lightbulb.SlashContext) -> None:    
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    """Skips the current song."""

    skip = await plugin.bot.d.lavalink.skip(ctx.guild_id)
    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    if not skip:
        await ctx.respond("Nothing to skip")
    else:
        # If the queue is empty, the next track won't start playing (because there isn't any),
        # so we stop the player.
        if not node.queue and not node.now_playing:
            await plugin.bot.d.lavalink.stop(ctx.guild_id)

        embed = (hikari.Embed(
            description=f"Skipped: **{skip.track.info.title}**",
            color=0x5deb1f
        ))
        await ctx.respond(embed)


@plugin.command()
@lightbulb.command("pause", "Pauses the current song.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pause(ctx: lightbulb.SlashContext) -> None:
    
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    """Pauses the current song."""

    await plugin.bot.d.lavalink.pause(ctx.guild_id)

    embed = (hikari.Embed(
        title="Paused player",
        description="You can use /resume to resume the song.",
        color=0xfa2617
    ))


    await ctx.respond(embed)


@plugin.command()
@lightbulb.command("resume", "Resumes playing the current song.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def resume(ctx: lightbulb.SlashContext) -> None:
    """Resumes playing the current song."""    
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    embed = (hikari.Embed(
        title="Resumed player",
        color=0x5deb1f
    ))


    await plugin.bot.d.lavalink.resume(ctx.guild_id)
    await ctx.respond(embed)


@plugin.command()
@lightbulb.command("nowplaying", "Gets the song that's currently playing.", aliases=["np"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def now_playing(ctx: lightbulb.SlashContext) -> None:
    """Gets the song that's currently playing."""
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    embed = (hikari.Embed(
        color=Color.from_rgb(r_g, r_b, r_r)
    ))

    if not node or not node.now_playing:
        embed.add_field(name="Playing:",value="Nothing is playing at the moment")
        await ctx.respond(embed)
        return

    # for queue, iterate over `node.queue`, where index 0 is now_playing.
    embed.add_field(name="Playing:", value=f"{node.now_playing.track.info.title}")
    
    await ctx.respond(embed)

@plugin.command()
@lightbulb.set_help("Gets the queque of the curretly songs.")
@lightbulb.command("queue", "Gets the songs in the queue")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_queue(ctx: lightbulb.SlashContext) -> None:
    states = plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == 892053033792454727 or i.user_id == ctx.member.id)]

    try:
        if not voice_state[0].channel_id == voice_state[1].channel_id:
            await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
            return

    except IndexError:
        await ctx.respond("You need to be on the same voice chat as saiki.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.queue:
        await ctx.respond("There are no tracks in the queue.")
        return

    r_g = random.randint(1, 255)
    r_b = random.randint(1, 255)
    r_r = random.randint(1, 255)

    embed = (
        hikari.Embed(
            title="Queue",
            description=f"Showing {len(node.queue)} song(s).",
            color=Color.from_rgb(r_g, r_b, r_r)
        )
        .add_field(name="Now playing", value=node.queue[0].track.info.title)
    )

    if len(node.queue) > 1:
        embed.add_field(name="Next up", value="\n".join(tq.track.info.title for tq in node.queue[1:]))

    await ctx.respond(embed)



@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)  # Optional
@lightbulb.option(
    "args", "The arguments to write to the node data.", required=False, modifier=lightbulb.OptionModifier.CONSUME_REST
)
@lightbulb.command("data", "Load or read data from the node.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def data(ctx: lightbulb.Context) -> None:
    """Load or read data from the node.
    If just `data` is ran, it will show the current data, but if `data <key> <value>` is ran, it
    will insert that data to the node and display it."""

    node = await plugin.bot.d.lavalink.get_guild_node(ctx.guild_id)

    if not node:
        await ctx.respond("No node found.")
        return None

    if args := ctx.options.args:
        args = args.split(" ")

        if len(args) == 1:
            node.set_data({args[0]: args[0]})
        else:
            node.set_data({args[0]: args[1]})
    await ctx.respond(node.get_data())


if HIKARI_VOICE:

    @plugin.listener(hikari.VoiceStateUpdateEvent)
    async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
        plugin.bot.d.lavalink.raw_handle_event_voice_state_update(
            event.state.guild_id,
            event.state.user_id,
            event.state.session_id,
            event.state.channel_id,
        )

    @plugin.listener(hikari.VoiceServerUpdateEvent)
    async def voice_server_update(event: hikari.VoiceServerUpdateEvent) -> None:
        await plugin.bot.d.lavalink.raw_handle_event_voice_server_update(event.guild_id, event.endpoint, event.token)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)