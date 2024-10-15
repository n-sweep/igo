import os
import asyncio
import discord
import concurrent.futures
from discord.ext import commands

from src.baduk import OGSGame

B = "⚫"
W = "⚪"

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
        f"# [{game.meta['GN']}](<{game.meta['PC'].split(' ')[1]}>) "
        "## (In progress)" if game.meta['RE'] == '?' else f"({game.meta['RE']})\n",
        f"`{B}` {p1}",
        f"`{W}` {p2}",
    ]
    return '\n'.join(lines)


class Base(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, *args):
        print()

    @commands.command(name='game')
    async def game_snapshot(self, ctx, *args):
        game = OGSGame(args[0])

        img_loc = game.snapshot()
        with open(img_loc, 'rb') as f:
            img = discord.File(f, filename=os.path.basename(img_loc))

        channels = {c.name: c for c in ctx.guild.channels}
        msg = build_title(ctx, game)
        await channels[gif_channel].send(msg, file=img)

    @commands.command()
    async def gif(self, ctx, *args):
        game = OGSGame(args[0])
        dur = 0.25

        if len(args) > 1:
            if args[1].isdigit():
                dur = float(args[1])
            elif args[1].lower() in ['fast', 'slow']:
                dur = {'fast': 0.05, 'slow': 1.5}
            else:
                print('invalid duration value', args[1])

        msg = f'Hi {ctx.author.mention}, your gif of game `{game.id}` is being created (a long game may take a few minutes)'
        await ctx.send(msg)

        gif_loc = await run_in_process(game.create_gif, dur)
        with open(gif_loc, 'rb') as f:
            gif = discord.File(f, filename=os.path.basename(gif_loc))

        channels = {c.name: c for c in ctx.guild.channels}
        msg = build_title(ctx, game)
        await channels[gif_channel].send(msg, file=gif)


class Bot(commands.Bot):
    def __init__(self, token: str):
        super().__init__(command_prefix='!', intents=intents)
        self.token = token

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.add_cog(Base(self))

    def run(self, *args, **kwargs):
        super().run(self.token, *args, **kwargs)


def main():
    with open('/home/n/.config/discord/bots/gobot/token', 'r') as f:
        token = f.read().strip()
    bot = Bot(token)
    bot.run()


if __name__ == '__main__':
    main()
