import os
import asyncio
import httpx
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "8614216581:AAEzpGkNOPtgQABf_mqXcjrAWM_RDT1Bpy8")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Видео курса — заполним после загрузки
VIDEOS = [
    # {"title": "Урок 1 — Танец", "file_id": "BAACAgI..."},
]

paid_users = set()


async def api(method, **kwargs):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{BASE_URL}/{method}", json=kwargs)
        return r.json()


async def send_message(chat_id, text, parse_mode="Markdown"):
    return await api("sendMessage", chat_id=chat_id, text=text, parse_mode=parse_mode)


async def send_video(chat_id, file_id, caption=""):
    return await api("sendVideo", chat_id=chat_id, video=file_id, caption=caption, parse_mode="Markdown")


async def handle_update(update):
    msg = update.get("message")
    if not msg:
        return

    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    first_name = msg["from"].get("first_name", "")
    text = msg.get("text", "")

    # Видео от админа — возвращаем file_id
    if user_id == ADMIN_ID and (msg.get("video") or msg.get("document")):
        v = msg.get("video") or msg.get("document")
        file_id = v["file_id"]
        await send_message(chat_id, f"✅ file\\_id:\n`{file_id}`")
        return

    if text == "/start":
        if user_id in paid_users:
            await send_course(chat_id)
        else:
            await send_message(chat_id,
                f"Привет, {first_name}\\! 👋\n\n"
                "Это курс Ле — танец, философия и мудры\\.\n\n"
                "💳 Стоимость: *XXXX₽*\n"
                "Реквизиты: *XXXX*\n\n"
                f"После оплаты напиши свой ID: `{user_id}`\n"
                "И я открою тебе доступ ✨",
                parse_mode="MarkdownV2"
            )

    elif text == "/myid":
        await send_message(chat_id, f"Твой ID: `{user_id}`")

    elif text.startswith("/give") and user_id == ADMIN_ID:
        parts = text.split()
        if len(parts) < 2:
            await send_message(chat_id, "Используй: /give USER\\_ID")
            return
        try:
            target_id = int(parts[1])
            paid_users.add(target_id)
            await send_message(chat_id, f"✅ Доступ выдан {target_id}")
            await send_message(target_id, "🎉 Оплата получена\\! Напиши /start чтобы получить курс", parse_mode="MarkdownV2")
        except Exception as e:
            await send_message(chat_id, f"Ошибка: {e}")

    elif text.startswith("/users") and user_id == ADMIN_ID:
        if paid_users:
            ids = "\n".join(str(u) for u in paid_users)
            await send_message(chat_id, f"Пользователи с доступом:\n{ids}")
        else:
            await send_message(chat_id, "Пока никому не выдан доступ")


async def send_course(chat_id):
    await send_message(chat_id,
        "✨ Доступ открыт\\! Отправляю материалы курса\\.\\.\\.\n\nСохрани этот чат — здесь все уроки 🙏",
        parse_mode="MarkdownV2"
    )
    if not VIDEOS:
        await send_message(chat_id, "⏳ Видео скоро будут здесь\\!", parse_mode="MarkdownV2")
        return
    for video in VIDEOS:
        await send_video(chat_id, video["file_id"], f"*{video['title']}*")
        await asyncio.sleep(0.5)


async def poll():
    offset = None
    logger.info("Бот запущен!")
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            async with httpx.AsyncClient(timeout=40) as client:
                r = await client.post(f"{BASE_URL}/getUpdates", json=params)
                data = r.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                await handle_update(update)
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(poll())
