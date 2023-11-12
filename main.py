import random
import praw
import json
import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix='Reda', intents=discord.Intents.all())
with open("settings.json", "r") as f:
    Token = json.load(f)
    TOKEN = Token["DISCORD_TOKEN"]


@bot.event
async def on_ready():
    print('Logged in lol'.format(bot))
    try:
        synced = await bot.tree.sync()
        print(f'synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


# Defining a command function to set up the bot.
@bot.tree.command(name="setup")
@app_commands.describe(client_id='Enter your client ID', client_secret='Enter your client secret',
                       username='Enter your reddit username without u/', password='Enter your reddit password')
async def setup(interaction: discord.Interaction, client_id: str, client_secret: str, username: str, password: str):
    new_user_data = {str(interaction.guild.id): [
        client_id, client_secret, f'bot by u/{username}', username, password
    ]
    }
    try:
        with open("info.json", "r") as f:
            info = json.load(f)
        id_check = info[f"{interaction.guild.id}"][0]
        # noinspection PyUnresolvedReferences
        await interaction.response.send_message("You have already setup your API.")
    except:
        try:
            with open("info.json", "r") as f:
                data = json.load(f)
                data.append(new_user_data)
            with open("info.json", "w") as f:
                json.dump(data, f, indent=4)
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message("Setup done successfully.")
        except Exception:
            print(Exception)
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message("Couldn't setup your API. Try again.")


# # Defining a command function to help the user with setting up the bot.
# @bot.tree.command(name="setuphelp")
# async def setuphelp(interaction: discord.Interaction):
#    embed = discord.Embed(
#        colour=discord.Colour.blurple(),
#        title="A tutorial on how to set up your API",
#        description="API LINK HERE",
#    )
#    embed.set_author(name="reddit.com/prefs/apps/", url="https://www.reddit.com/prefs/apps/")
#    # noinspection PyUnresolvedReferences
#    await interaction.response.send_message(embed=embed)


# Defining a command function to acquire a random post from top 100 of the day.
@bot.tree.command(name="acquire")
@app_commands.describe(subreddit="Enter the subreddit from which you want the post")
async def acquire(interaction: discord.Interaction, subreddit: str):
    with open("info.json", "r") as f:
        info = json.load(f)
    for item in info:
        if str(interaction.guild.id) in item:
            client_id = item[str(interaction.guild.id)][0]
            client_secret = item[str(interaction.guild.id)][1]
            user_agent = item[str(interaction.guild.id)][2]
            username = item[str(interaction.guild.id)][3]
            password = item[str(interaction.guild.id)][4]
            break

    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(f"Acquiring a post from r/{subreddit}...")
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        sub = reddit.subreddit(subreddit)
        posts = sub.top(time_filter="day", limit=100)  # Change time_filter to change the duration from which the top
        # posts are acquired, limit to change the number of posts to acquire.
        post = list(posts)
        post = random.choice(post)
        if post.over_18:
            if interaction.channel.is_nsfw():
                post_embed = discord.Embed(
                    colour=discord.Colour.red()
                )
                post_embed.set_author(name=post.title, url=post.url)
                post_embed.set_image(url=post.url)
                post_embed.set_footer(text="If the image doesn't load, it could be a video or a text post.")
                await interaction.channel.send(embed=post_embed)
            else:
                await interaction.channel.send("This post can be viewed only in NSFW channels.")
        else:
            post_embed = discord.Embed(
                colour=discord.Colour.red()
            )
            post_embed.set_author(name=post.title, url=post.url)
            post_embed.set_image(url=post.url)
            post_embed.set_footer(text="If the image doesn't load, it could be a video or a text post.")
            await interaction.channel.send(embed=post_embed)
    except Exception:
        print(Exception)
        await interaction.channel.send(
            "Couldn't acquire a post, reasons could be incorrect credentials or subreddit doesn't exist.")


bot.run(TOKEN)
