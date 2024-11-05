import os
import asyncio
import discord
import logging
import concurrent.futures
from discord.ext import commands

from src.baduk import OGSGame
from src.util import find_ogs_user

B = "⚫"
W = "⚪"

logger = logging.getLogger('discord')

gif_channel = 'testing-ground'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def run_in_process(func, *args):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


def build_title(ctx, game):
    users = {item: m for m in ctx.guild.members for item in (m.name, m.nick)}
    p1 = game.p1_username
    p2 = game.p2_username
    p1 = f"{users[p1].mention}" if p1 in users else p1
    p2 = f"{users[p2].mention}" if p2 in users else p2

    lines = [
        f"# [{game.meta['GN']}](<{game.meta['PC'].split(' ')[1]}>) ",
        "## (In progress)" if game.meta['RE'] == '?' else f"({game.meta['RE']})\n",
        f"`{B}` {p1}",
        f"`{W}` {p2}",
    ]
    return '\n'.join(lines)


class Base(commands.Cog):
    def __init__(self, bot: commands.Bot, img_channel: str|None = None):
        self.bot = bot
        self.img_channel = img_channel

    @commands.command()
    async def test(self, ctx, *args):
        ...

    @commands.command()
    async def ogs_users(self, ctx):
        """Looks for users with matching OGS usernames and gives them the OGS role"""
        ogs_role = {r.name: r for r in ctx.guild.roles}['OGS']

        for member in (b for b in self.bot.get_all_members() if not b.bot):

            if 'OGS' not in [r.name for r in member.roles]:
                logger.info(member)

                results = find_ogs_user(name:=member.display_name.lower())
                if not results and member.name != name:
                    results = find_ogs_user(name:=member.name.lower())

                if not (results:={r['username'].lower(): r for r in results}):
                    logger.info(f'{name}: no matching users found')
                elif name in results:
                    logger.info(f'{name}: OGS role added')
                    await member.add_roles(ogs_role)
                else:
                    logger.info(f'{name}: similar matches found: {list(results.keys())}')

    @commands.command(name='game')
    async def game_snapshot(self, ctx, *args):
        try:
            game = OGSGame(args[0])
        except:
            logger.info(f'private game {args[0]}...')
            await ctx.reply("Sorry, I cannot access private games.")
            return

        logger.info(f'creating png {game.id}...')
        img_loc = game.snapshot()
        with open(img_loc, 'rb') as f:
            img = discord.File(f, filename=os.path.basename(img_loc))

        msg = build_title(ctx, game)
        await ctx.reply(msg, file=img)

    @commands.command()
    async def gif(self, ctx, *args):
        try:
            game = OGSGame(args[0])
        except:
            logger.info(f'private game {args[0]}...')
            await ctx.reply("Sorry, I cannot access private games.")
            return

        dur = 0.25

        if len(args) > 1:
            if args[1].isdigit():
                dur = float(args[1])
            elif args[1].lower() in ['fast', 'slow']:
                dur = {'fast': 0.05, 'slow': 1.5}[args[1]]
            else:
                logger.info(f'invalid duration value {args[1]}')

        msg = f"Hi {ctx.author.mention}, your gif of game `{game.id}` is being generated. This can take me several minutes, I will ping you when it's complete!"
        await ctx.reply(msg)

        logger.info(f'creating gif {game.id}...')
        gif_loc = await run_in_process(game.create_gif, dur)
        with open(gif_loc, 'rb') as f:
            gif = discord.File(f, filename=os.path.basename(gif_loc))

        msg = build_title(ctx, game)
        await ctx.reply(msg, file=gif)


class Bot(commands.Bot):
    def __init__(self, token: str):
        super().__init__(command_prefix='!', intents=intents)
        self.token = token

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')
        await self.add_cog(Base(self))

    def run(self, *args, **kwargs):
        super().run(self.token, *args, **kwargs)
