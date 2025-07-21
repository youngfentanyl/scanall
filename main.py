import discord
from discord.ext import commands
from pypresence import Presence
import asyncio
import time

TOKEN = "MTM5NDgwODYzNDU3OTQ4ODg2OQ.GKomDy.Ty1AU3A2K_NvfDCM2c_A-Lim5ow5STeMMX7dkw"# Remplace par ton token bot Discord
CLIENT_ID = "1394808634579488869"      # ID de ton application Discord (pour Rich Presence)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

RPC = Presence(CLIENT_ID)  # Client Rich Presence


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user} !')

    # Connecte le client Rich Presence
    RPC.connect()

    # Met à jour la Rich Presence
    RPC.update(
        details="In This Shirt",
        state="The Irrepressibles",
        large_image="ab67616d0000b273ad788be5a21e95bd6020ce74",
        large_text="Écoute sur Spotify",
        start=time.time()
    )
    print("Rich Presence activée.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")

# Pour garder le client RPC actif sans bloquer le bot
async def keep_rpc_alive():
    while True:
        try:
            RPC.update()
        except Exception:
            pass
        await asyncio.sleep(15)

async def main():
    asyncio.create_task(keep_rpc_alive())
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
