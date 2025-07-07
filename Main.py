import os
import aiohttp
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import time

# GitHub Secrets سے حاصل ہونے والی اقدار
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://1waqhg.life/casino/play/spribe_aviator?p=e9g9"  # درست URL

bot = Bot(token=BOT_TOKEN)

async def get_latest_crash():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # تمام کریش پوائنٹس تلاش کریں
                crash_elements = soup.find_all("div", class_="crash-point")
                
                if crash_elements:
                    # آخری کریش ویلیو حاصل کریں
                    crash = crash_elements[-1].text.strip()
                    return crash
                return "کوئی ڈیٹا نہیں ملا"
    except Exception as e:
        return f"خرابی: {str(e)}"

async def send_crash_update():
    result = await get_latest_crash()
    message = f"✈️ اویئٹر کریش سگنل: {result}"
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    while True:
        await send_crash_update()
        await asyncio.sleep(30)  # 30 سیکنڈ انتظار

if __name__ == "__main__":
    asyncio.run(main())
