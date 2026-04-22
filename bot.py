import os
import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "8614216581:AAEzpGkNOPtgQABf_mqXcjrAWM_RDT1Bpy8")
ADMIN_ID = int(os.getenv("ADMIN_ID", "429779513"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

VIDEOS = [
    {"title": "Видео 1", "file_id": "BAACAgIAAxkBAAMKaegJQEDBNymLLuzGoagPG6RgLYgAAvKiAAJF70BL8r7eZD3PoI07BA", "text": "Заменить подпись"},
    {"title": "Видео 2", "file_id": "BAACAgIAAxkBAAMMaegJllv4SxgjvvQ9CbFxcCbJJm4AAvOiAAJF70BLCcWT0jpS55w7BA", "text": "Заменить подпись"},
    {"title": "Видео 3", "file_id": "BAACAgIAAxkBAAMOaegJudNX_gIKqD5SEpio4i6GnbgAAvSiAAJF70BLsOWPxytEDtg7BA", "text": "Заменить подпись"},
    {"title": "Видео 4", "file_id": "BAACAgIAAxkBAAMQaegKOkt8xrwsnk0FidG7fOg8T0MAAvWiAAJF70BLEskdgPhjyV87BA", "text": "Заменить подпись"},
    {"title": "Видео 5", "file_id": "BAACAgIAAxkBAAMSaegLXBTDZGOGOYtCRkYdgErDvdEAAveiAAJF70BLPmMAAbCRwgMgOwQ", "text": "Заменить подпись"},
    {"title": "Видео 6", "file_id": "BAACAgIAAxkBAAMUaegLsw2xa8BTVGksQswGnj4auxUAAviiAAJF70BLIqQqefLhg-47BA", "text": "Заменить подпись"},
]


async def api(method, **kwargs):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{BASE_URL}/{method}", json=kwargs)
        return r.json()


async def send_message(chat_id, text, reply_markup=None):
    params = dict(chat_id=chat_id, text=text, parse_mode="Markdown")
    if reply_markup:
        params["reply_markup"] = reply_markup
    return await api("sendMessage", **params)


async def send_video(chat_id, file_id, caption=""):
    return await api("sendVideo", chat_id=chat_id, video=file_id, caption=caption, parse_mode="Markdown")


async def handle_update(update):
    # Кнопка
    callback = update.get("callback_query")
    if callback:
        chat_id = callback["message"]["chat"]["id"]
        if callback["data"] == "start_course":
            await api("answerCallbackQuery", callback_query_id=callback["id"])
            await send_course(chat_id)
        return

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
        await send_message(chat_id, f"✅ file\\_id:\n`{v['file_id']}`")
        return

    if text == "/start":
        reply_markup = {
            "inline_keyboard": [[
                {"text": "✨ Начать курс", "callback_data": "start_course"}
            ]]
        }
        await send_message(chat_id,
            f"Привет, {first_name}! 👋\n\n"
            "Добро пожаловать в курс Ле.\n\n"
            "Здесь тебя ждут уроки танца, философии и мудр.\n\n"
            "Нажми кнопку ниже чтобы начать 👇",
            reply_markup=reply_markup
        )

    elif text == "/myid":
        await send_message(chat_id, f"Твой ID: `{user_id}`")


async def send_course(chat_id):
    await send_message(chat_id, "✨ Отправляю материалы курса...\n\nСохрани этот чат — здесь все уроки 🙏")
    for video in VIDEOS:
        caption = f"*{video['title']}*\n\n{video['text']}"
        await send_video(chat_id, video["file_id"], caption)
        await asyncio.sleep(1)
    await send_message(chat_id, "🎉 Это все материалы курса!\n\nЕсли есть вопросы — пиши Ле напрямую.")


async def poll():
    offset = None
    logger.info("Бот запущен!")
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
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
