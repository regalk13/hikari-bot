# Hikari Bot

A discord bot written in python using hikari and several libraries that add more features to hikari.

You can add the bot [here](https://discord.com/oauth2/authorize?client_id=892053033792454727&permissions=8&scope=bot%20applications.commands).


🍃 _Saiki Free & open and powerfull_ 🍃


# Running the bot

## Installing dependencies

You will need Python 3.10 or higher to run this bot () 

```
# To run the bot:
pip install -r requirements.txt
python -m testbot
```
Use CTRL+C to shut the bot down.


## Using hikari & lightbulb

```python
# Import the command handler
import lightbulb

# Instantiate a Bot instance
bot = lightbulb.BotApp(token="your_token_here", prefix="your_prefix_here")

# Register the command to the bot
@bot.command
# Use the command decorator to convert the function into a command
@lightbulb.command("ping", "checks the bot is alive")
# Define the command type(s) that this command implements
@lightbulb.implements(lightbulb.PrefixCommand)
# Define the command's callback. The callback should take a single argument which will be
# an instance of a subclass of lightbulb.context.Context when passed in
async def ping(ctx: lightbulb.Context) -> None:
    # Send a message to the channel the command was used in
    await ctx.respond("Pong!")

# Run the bot
# Note that this is blocking meaning no code after this line will run
# until the bot is shut off
bot.run()
```
## Using the database

If you need to create a new table for the database, follow the naming convention set out in the data/static/build.sql file.

The database utility is now very different. Examples below:

```py
# Inserting data (from plugin)
await plugin.bot.d.db.execute("INSERT INTO ... VALUES ...", ...)

# Selecting data (from plugin)
row = await plugin.bot.d.db.try_fetch_record("SELECT user_id, points FROM experience WHERE user_id = ?", ...)
print(row.user_id)
print(row.points)
```

Datetime objects are automatically converted both ways, so fetching a field with a time in it will return a datetime object, and passing a datetime object to `execute` will insert a string timestamp.

```py
import datetime as dt

expires = await plugin.bot.d.db.try_fetch_field("SELECT expires FROM warnings WHERE user_id = ?")
isinstance(expires, dt.datetime) == True
```

# Creating a bot or Contributing

Check the docs of this dependencies:

https://www.hikari-py.dev/hikari/

https://hikari-lightbulb.readthedocs.io/en/latest/

https://tanjun.cursed.solutions/release/index.html

https://vicky5124.github.io/lavasnek_rs/lavasnek_rs/lavasnek_rs.html

If you have ideas for new commands you can add them with a pull request, or refactor my code.

# License
MIT
