
import os
import discord
from discord.ext import commands

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

@bot.event
async def on_ready():
    print(f"SNTY ONLINE: {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message: str):
    if not CHANNEL_ID:
        return await ctx.reply("Channel ID is not configured.")

    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        return await ctx.reply("Channel not found.")

    await channel.send(message)
    await ctx.reply("SNTY announcement sent!")

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("Administrator permission required.")
    else:
        await ctx.reply("Unable to send announcement.")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing.")

bot.run(TOKEN)
