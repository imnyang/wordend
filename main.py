import os
import discord
import aiohttp
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message is sent by the bot itself
        return  # Ignore the message

    if message.channel.id == 1272817370054000751:
        if message.content.startswith("!"):
            pass
        word = message.content
        response = f"https://kkutu.io/dict/{word}?lang=ko"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(response) as resp:
                    data = await resp.json()
                    print(data)
                    if "error" in data:
                        await message.add_reaction("❌")
                        reply_message = await message.reply(f"`{word}`라는 단어가 존재하지 않습니다. (2초뒤 삭제됩니다.)")
                        await asyncio.sleep(2)
                        await message.delete()
                        await reply_message.delete()
                    else:
                        if word.endswith("늄") or word.endswith("듐") or word.endswith("튬") or word.endswith("륨") or word.endswith("븀"):
                            await message.add_reaction("❌")
                            reply_message = await message.reply(f"`{word[-1]}`으로 끝나는 단어는 사용할 수 없습니다. (2초뒤 삭제됩니다.)")
                            await asyncio.sleep(2)
                            await message.delete()
                            await reply_message.delete()
                        else:
                            await message.add_reaction("✅")
        except Exception as e:
            print(f"An error occurred: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))