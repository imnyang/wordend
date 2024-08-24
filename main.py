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

async def fetch(word):
    url = f"https://kkutu.co.kr/o/dict/{word}?lang=ko"
    headers = {
        "Host": "kkutu.co.kr",
        "Cookie": os.getenv('KKUTU_COOKIE'),
        "Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR",
        "Sec-Ch-Ua-Mobile": "?0",
        "Authorization": os.getenv('KKUTU_TOKEN'),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://kkutu.co.kr/o/game?server=7",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message is sent by the bot itself
        return  # Ignore the message



    if message.channel.id == 1272817370054000751:
        if message.content.startswith("!"):
            return
        word = message.content

        try:
            data = await fetch(word)
            print(word)
            print(str(data))
            if "error" in data:
                await message.add_reaction("❌")
                reply_message = await message.reply(f"`{word}`라는 단어가 존재하지 않습니다. (2초뒤 삭제됩니다.)")
                await asyncio.sleep(2)
                await message.delete()
                await reply_message.delete()
            else:
                if word.endswith("늄") or word.endswith("듐") or word.endswith("튬") or word.endswith("륨") or word.endswith("븀") or word.endswith("쾨"):
                    await message.add_reaction("❌")
                    reply_message = await message.reply(f"`{word[-1]}`으로 끝나는 단어는 사용할 수 없습니다. (2초뒤 삭제됩니다.)")
                    await asyncio.sleep(2)
                    await message.delete()
                    await reply_message.delete()
                else:
                    await message.add_reaction("✅")
        except Exception as e:
            await message.add_reaction("✅")
            await message.add_reaction("❓")
            print(f"An error occurred: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))