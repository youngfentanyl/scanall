import os
import discord
from discord.ext import commands
import re
import aiohttp
from collections import Counter

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Missing DISCORD_TOKEN environment variable.")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='r!', intents=intents)

invite_regex = re.compile(r'(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite)\/[A-Za-z0-9]+')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def scanall(ctx, message_id: int):
    await ctx.send("Scanning messages, please wait...")

    channel = ctx.channel
    links_found = []

    try:
        ref_message = await channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Message ID not found.")
        return

    async for message in channel.history(after=ref_message, oldest_first=True, limit=None):
        matches = invite_regex.findall(message.content)
        for match in matches:
            full_url = match[0] + match[1] + match[2] + "/" + message.content.split(match[2] + "/")[1].split()[0]
            links_found.append(full_url)

    if not links_found:
        await ctx.send("No Discord invite links found.")
        return

    counts = Counter(links_found)
    session = aiohttp.ClientSession()

    results = []
    for link, count in counts.most_common():
        invite_code = link.split("/")[-1]

        async with session.get(f"https://discord.com/api/v10/invites/{invite_code}?with_counts=true") as resp:
            if resp.status == 200:
                data = await resp.json()
                member_count = data['approximate_member_count']
            else:
                member_count = "Unknown"

        results.append(f"**{link}** ({count} times) ({member_count} members)")

    await session.close()

    embed = discord.Embed(
        title="Scan finished",
        description="\n".join(f"#{i+1} {result}" for i, result in enumerate(results)),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)
