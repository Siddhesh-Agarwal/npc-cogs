import discord
from redbot.core.bot import Red
from redbot.core import commands
import json


class Reddit(commands.Cog):

    __version__ = "0.0.1"
    __author__ = "Siddhesh-Agarwal"

    def __init__(self, bot: Red):
        self.bot = bot
        self.BASE_URL = "https://www.reddit.com"

    @commands.group(invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def reddit(self, subreddit: str = "ProgrammerHumor", limit: int = 3):
        """
        Get the top posts from a subreddit.
        """
        if limit > 25:
            limit = 25
        elif limit < 1:
            limit = 1
        subreddit = subreddit.lower()
        url = f"{self.BASE_URL}/r/{subreddit}/top.json?limit={limit}"

        async with self.bot.session.get(url) as resp:
            if resp.status != 200:
                return await self.bot.say("Could not get data from reddit.")
            data = await resp.json()
            if not data["data"]["children"]:
                return await self.bot.say("No posts found.")
            embed = discord.Embed(title=f"Top {limit} posts from r/{subreddit}")
            for post in data["data"]["children"]:
                post_data = json.loads(post["data"])
                embed.add_field(
                    name=post_data["title"],
                    value=f"{self.BASE_URL}{post_data['permalink']}",
                    inline=False,
                )
            await self.bot.say(embed=embed)
