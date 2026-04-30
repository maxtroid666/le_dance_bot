import os
import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "8614216581:AAEzpGkNOPtgQABf_mqXcjrAWM_RDT1Bpy8")
ADMIN_ID = int(os.getenv("ADMIN_ID", "429779513"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

INTRO_TEXT = """В праславянском языке слово «ведьма» не несло никакого тёмного смысла. Оно буквально означало «ведающая» — та, что знает. Корень «вед» — тот же, что в санскритском «веда» (священное знание). Ведающая женщина была хранительницей рода, знахаркой, мудрецом — той, к кому приходили за советом, потому что она видела то, что скрыто от других.
Это прямое знание. Не выученное. Не переданное через книги или чужой опыт. Знание, которое приходит изнутри — через тело, через ощущение, через связь с чем-то большим, чем личная история.
Женщина-творец — это та, кто создаёт реальность не усилием воли, а из этой глубины. Она не подстраивается под мир — она формирует его. Её хореография — это не набор движений. Это язык, которым говорит архетип (изначальный образ, живущий в коллективном бессознательном): я здесь, я знаю, я создаю.
Юнг (Карл Густав Юнг, швейцарский психолог) описывал архетипы как универсальные образы, заложенные в психике каждого человека. Архетип Творца — один из самых редких и самых мощных. Это тот, кто превращает невидимое в видимое. Воображаемое — в реальное. Внутренний импульс — в форму, в движение, в жизнь.
В этом видео — разбор хореографии, которая воплощает именно этот образ. Как через тело войти в роль женщины, которая не ждёт — а создаёт. Не просит — а знает. Не ищет себя — а уже есть."""

BONUS_TEXT = """Дополнительная хореография "Танец обольщения короля" (бонусное видео)"""

VIDEOS = [
    {"file_id": "BAACAgIAAxkBAAN-afKfIzQgC_LvCYds6GOsH29JwLkAAgifAALl5ZhLr5yIK1AxCl47BA", "text": ""},
    {"file_id": "BAACAgIAAxkBAAMKaegJQEDBNymLLuzGoagPG6RgLYgAAvKiAAJF70BL8r7eZD3PoI07BA", "text": 'История создания хореографии "WHEY CALL ME A WITCH"'},
    {"file_id": "BAACAgIAAxkBAAMMaegJllv4SxgjvvQ9CbFxcCbJJm4AAvOiAAJF70BLCcWT0jpS55w7BA", "text": 'Разбор хореографии "WHEY CALL ME A WITCH". Сидячее положение'},
    {"file_id": "BAACAgIAAxkBAAMOaegJudNX_gIKqD5SEpio4i6GnbgAAvSiAAJF70BLsOWPxytEDtg7BA", "text": """В теле человека насчитывается более 400 биологически активных точек — БАТ. Тысячелетиями китайская медицина и восточные практики работали с ними через акупунктуру (иглоукалывание) и акупрессуру (точечное воздействие): каждая точка — это ворота, через которые движется тонкая энергия, ци (жизненная сила). Когда эти ворота закрыты — тело напряжено, поле сжато, человек отрезан от потока.
Но есть и другое измерение этого знания.
Большинство людей защищают себя через границы: выстраивают стены, закрываются, уходят в броню. Это понятная, но слабая стратегия — потому что любую стену можно пробить. Именно там, где есть граница, есть и цель для удара.
Древний даосский принцип у-вэй (недеяние, растворение в потоке) говорит об обратном: сила — в пустоте. Когда ты раскрыт настолько, что тебя как отдельного объекта больше нет — ты становишься всем. А то, чего нет, невозможно задеть.
Это и есть техника раскрытия БАТ — самая неожиданная и самая мощная форма защиты. Не стена. Не броня. Не контроль. А полное растворение — в своей личной правде, в божественном, в информации, которая всегда была рядом, но не могла достучаться сквозь напряжение закрытого тела.
Когда точки открыты — ты максимально восприимчив. К себе. К партнёру. К тому, что хочет прийти через тебя.
В этом видео — практика, которая помогает именно это и сделать."""},
    {"file_id": "BAACAgIAAxkBAAMQaegKOkt8xrwsnk0FidG7fOg8T0MAAvWiAAJF70BLEskdgPhjyV87BA", "text": 'Разбор хореографии "WHEY CALL ME A WITCH". Стоячее положение'},
    {"file_id": "BAACAgIAAxkBAAMSaegLXBTDZGOGOYtCRkYdgErDvdEAAveiAAJF70BLPmMAAbCRwgMgOwQ", "text": """Тысячи лет назад существовали женщины, которых называли ganika (ганика) — высшие куртизанки древней Индии. Камасутра описывает их как хранительниц 64 искусств: пения, танца, алхимии запаха, искусства украшать тело и создавать пространство вокруг себя. Они были советницами королей, музами полководцев — женщинами, перед которыми невозможно было устоять.
Их секрет был не в красоте и не в теле.
Они знали: настоящее обольщение — это ритуал. Это энергия, намерение, преображение. Это когда ты не просто приходишь к мужчине — ты являешься ему. Как богиня. Как тайна. Как то, что он не может объяснить, но не может забыть.
Танец куртизанки — почти статичен. Он не требует хореографии или физических усилий. Аромасло — своё или его. Украшения на теле. Полное соединение с женским архетипом внутри себя. И — тантра во всём: каждое движение, каждый взгляд, каждый жест становится частью перформанса.
Потому что великие трактаты о любви говорят одно: занятие любовью между мужчиной и женщиной — это божественное мероприятие. И когда оно наполнено алхимией, волшебством и экстазом — это уже не просто близость. Это священный ритуал двоих.
В этом видео — одна из таких техник. Как создать прелюдию, которая заворожит и вдохновит. Как превратить обычный вечер в нечто, что он будет помнить всегда."""},
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

    # Видео 0 — без подписи
    await send_video(chat_id, VIDEOS[0]["file_id"], "")
    await asyncio.sleep(1)

    # Сообщение про ведьму/архетип
    await send_message(chat_id, INTRO_TEXT)
    await asyncio.sleep(1)

    # Видео 1 — История создания
    await send_video(chat_id, VIDEOS[1]["file_id"], VIDEOS[1]["text"])
    await asyncio.sleep(1)

    # Видео 2 — Сидячее положение
    await send_video(chat_id, VIDEOS[2]["file_id"], VIDEOS[2]["text"])
    await asyncio.sleep(1)

    # Видео 3 — БАТ
    await send_video(chat_id, VIDEOS[3]["file_id"], VIDEOS[3]["text"])
    await asyncio.sleep(1)

    # Видео 4 — Стоячее положение
    await send_video(chat_id, VIDEOS[4]["file_id"], VIDEOS[4]["text"])
    await asyncio.sleep(1)

    # Сообщение про бонусное видео
    await send_message(chat_id, BONUS_TEXT)
    await asyncio.sleep(1)

    # Видео 5 — Танец обольщения короля
    await send_video(chat_id, VIDEOS[5]["file_id"], VIDEOS[5]["text"])
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
