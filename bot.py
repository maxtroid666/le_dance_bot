import os
import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "8614216581:AAEzpGkNOPtgQABf_mqXcjrAWM_RDT1Bpy8")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ADMIN_IDS = {
    429779513,   # Макс
    5859444039,  # Ле
}

allowed_users = set()
started_chats = set()


async def api(method, **kwargs):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{BASE_URL}/{method}", json=kwargs)
        return r.json()


async def send_message(chat_id, text, reply_markup=None):
    params = dict(chat_id=chat_id, text=text)
    if reply_markup:
        params["reply_markup"] = reply_markup
    return await api("sendMessage", **params)


async def send_video(chat_id, file_id, caption=""):
    return await api("sendVideo", chat_id=chat_id, video=file_id, caption=caption)


async def show_start(chat_id, first_name, user_id):
    if user_id in ADMIN_IDS:
        await send_message(chat_id,
            f"Привет, {first_name}! Ты админ 👑\n\n"
            "Команды:\n"
            "/add 123456789 — добавить пользователя\n"
            "/remove 123456789 — убрать пользователя\n"
            "/list — список с доступом"
        )
        return

    keyboard = [
        [{"text": "🆔 Узнать мой ID"}],
        [{"text": "🔄 Проверить доступ"}]
    ]
    reply_markup = {
        "keyboard": keyboard,
        "resize_keyboard": True
    }
    await send_message(chat_id,
        f"Привет, {first_name}! 👋\n\n"
        "Добро пожаловать в курс Ле.\n\n"
        "⚠️ Доступ к курсу открывается после оплаты.\n\n"
        "Если ты уже оплатила — нажми «🆔 Узнать мой ID», скопируй цифры и отправь их Ле. "
        "После того как Ле добавит тебя, нажми «🔄 Проверить доступ» и курс откроется.",
        reply_markup=reply_markup
    )


async def send_course(chat_id):
    await api("sendMessage", chat_id=chat_id,
              text="✨ Отправляю материалы курса...\n\nСохрани этот чат — здесь все уроки 🙏",
              reply_markup={"remove_keyboard": True})

    await send_video(chat_id, "BAACAgIAAxkBAAPTafKuU-LYMaabB3NVoG6d1poV5UIAAiifAALl5ZhLXzsxVnyTbwU7BA")
    await asyncio.sleep(1)

    await send_message(chat_id,
        "В праславянском языке слово «ведьма» не несло никакого тёмного смысла. Оно буквально означало «ведающая» — та, что знает. "
        "Корень «вед» — тот же, что в санскритском «веда» (священное знание). Ведающая женщина была хранительницей рода, знахаркой, "
        "мудрецом — той, к кому приходили за советом, потому что она видела то, что скрыто от других.\n\n"
        "Это прямое знание. Не выученное. Не переданное через книги или чужой опыт. Знание, которое приходит изнутри — через тело, "
        "через ощущение, через связь с чем-то большим, чем личная история.\n\n"
        "Женщина-творец — это та, кто создаёт реальность не усилием воли, а из этой глубины. Она не подстраивается под мир, она формирует "
        "его. Её хореография — это язык, которым говорит архетип (изначальный образ, живущий в коллективном бессознательном): я здесь, я знаю, я создаю.\n\n"
        "Юнг (Карл Густав Юнг, швейцарский психолог) описывал архетипы как универсальные образы, заложенные в психике каждого человека. "
        "Архетип Творца — один из самых редких и самых мощных. Это тот, кто превращает невидимое в видимое. Воображаемое в реальное. "
        "Внутренний импульс в форму, в движение, в жизнь.\n\n"
        "В этом видео — разбор хореографии, которая воплощает именно этот образ. Как через тело войти в роль женщины, которая не ждёт, "
        "а создаёт. Не просит, а знает. Не ищет себя, а уже есть."
    )
    await asyncio.sleep(1)

    await send_video(chat_id,
        "BAACAgIAAxkBAAPVafKu3Ofyg7FHHdUjjsBhTPohLmgAAimfAALl5ZhLUB9ebAmC80o7BA",
        "Идея постановки «THEY CALL ME A WITCH»"
    )
    await asyncio.sleep(1)

    await send_message(chat_id,
        "В теле человека насчитывается более 400 биологически активных точек — БАТ. Тысячелетиями китайская медицина и восточные практики "
        "работали с ними через акупунктуру (иглоукалывание) и акупрессуру (точечное воздействие): каждая точка — это ворота, через которые "
        "движется тонкая энергия, ци (жизненная сила). Когда эти ворота закрыты, тело напряжено, поле сжато, человек отрезан от потока.\n\n"
        "Но есть и другое измерение этого знания.\n\n"
        "Большинство людей защищают себя через границы: выстраивают стены, закрываются, уходят в броню. Это понятная, но слабая стратегия — "
        "потому что любую стену можно пробить. Именно там, где есть граница, есть и цель для удара.\n\n"
        "Древний даосский принцип у-вэй (недеяние, растворение в потоке) говорит об обратном: сила в пустоте. Когда ты раскрыт настолько, "
        "что тебя как отдельного объекта больше нет — ты становишься всем. А то, чего нет, невозможно задеть."
    )
    await asyncio.sleep(1)

    await send_video(chat_id,
        "BAACAgIAAxkBAAPXafKvbF3ameNYOsysLI_ReQdtGZ4AAiqfAALl5ZhL3CbvMKsuyKE7BA",
        "Это и есть техника раскрытия БАТ — самая неожиданная и самая мощная форма защиты. Не стена. Не броня. Не контроль. А полное "
        "растворение в своей личной правде, в божественном, в информации, которая всегда была рядом, но не могла достучаться сквозь "
        "напряжение закрытого тела.\n\n"
        "Когда точки открыты, ты максимально восприимчив. К себе. К партнёру. К тому, что хочет прийти через тебя.\n\n"
        "В этом видео практика, которая помогает именно это и сделать."
    )
    await asyncio.sleep(1)

    inline_markup = {
        "inline_keyboard": [[{"text": "✨ Получить хореографию", "callback_data": "get_choreo"}]]
    }
    await send_message(chat_id, "Готова к разбору хореографии? 👇", reply_markup=inline_markup)


async def send_choreo(chat_id):
    await send_video(chat_id,
        "BAACAgIAAxkBAAPZafKvn_s1jB5uA4uEh5bRTCorVHkAAiufAALl5ZhLlsUosUUcpp47BA",
        "THEY CALL ME A WITCH\nРазбор хореографии (сидячее положение)"
    )
    await asyncio.sleep(1)

    await send_video(chat_id,
        "BAACAgIAAxkBAAPbafKw7UWYlGwrJwABiVel3ry6U0CYAAIsnwAC5eWYS23DbtHL3mnWOwQ",
        "THEY CALL ME A WITCH\nРазбор хореографии (стоячее положение)"
    )
    await asyncio.sleep(1)

    await send_message(chat_id,
        "Ниже я дала Вам дополнительный разбор хореографии под названием:\n«Танец для обольщения КОРОЛЯ»"
    )
    await asyncio.sleep(1)

    inline_markup = {
        "inline_keyboard": [[{"text": "💫 Получить дополнительные материалы", "callback_data": "get_bonus"}]]
    }
    await send_message(chat_id, "Нажми, чтобы получить бонус 👇", reply_markup=inline_markup)


async def send_bonus(chat_id):
    await send_message(chat_id,
        "Тысячи лет назад существовали женщины, которых называли ganika (ганика) — высшие куртизанки древней Индии. "
        "Камасутра описывает их как хранительниц 64 искусств: пения, танца, алхимии запаха, искусства украшать тело и создавать "
        "пространство вокруг себя. Они были советницами королей, музами полководцев — женщинами, перед которыми невозможно было устоять.\n\n"
        "Их секрет был не в красоте и не в теле.\n\n"
        "Они знали: настоящее обольщение — это ритуал. Это энергия, намерение, преображение. Это когда ты не просто приходишь к мужчине — "
        "ты являешься ему. Как богиня. Как тайна. Как то, что он не может объяснить, но не может забыть.\n\n"
        "Танец куртизанки — почти статичен. Он не требует хореографии или физических усилий. Аромасло — своё или его. Украшения на теле. "
        "Полное соединение с женским архетипом внутри себя. И — тантра во всём: каждое движение, каждый взгляд, каждый жест становится частью перформанса.\n\n"
        "Потому что великие трактаты о любви говорят одно: занятие любовью между мужчиной и женщиной — это божественное мероприятие. "
        "И когда оно наполнено алхимией, волшебством и экстазом — это уже не просто близость. Это священный ритуал двоих.\n\n"
        "В этом видео — одна из таких техник. Как создать прелюдию, которая заворожит и вдохновит. "
        "Как превратить обычный вечер в нечто, что он будет помнить всегда."
    )
    await asyncio.sleep(1)

    await send_video(chat_id,
        "BAACAgIAAxkBAAPdafKxe-sTSPrGChvZ1Z1O12nfDS8AAi2fAALl5ZhLtVCNtya6VvA7BA",
        "«Танец для обольщения КОРОЛЯ»\n(Бонусное видео)"
    )
    await asyncio.sleep(1)

    await send_message(chat_id, "🎉 Это все материалы курса!\n\nЕсли есть вопросы — пиши Ле напрямую.")


async def handle_update(update):
    callback = update.get("callback_query")
    if callback:
        chat_id = callback["message"]["chat"]["id"]
        data = callback["data"]
        await api("answerCallbackQuery", callback_query_id=callback["id"])
        if data == "get_choreo":
            await send_choreo(chat_id)
        elif data == "get_bonus":
            await send_bonus(chat_id)
        return

    msg = update.get("message")
    if not msg:
        return

    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    first_name = msg["from"].get("first_name", "")
    text = msg.get("text", "").strip()

    # Админ загружает видео — возвращаем file_id
    if user_id in ADMIN_IDS and (msg.get("video") or msg.get("document")):
        v = msg.get("video") or msg.get("document")
        await send_message(chat_id, "file_id:\n" + v["file_id"])
        return

    # Команды для админов
    if user_id in ADMIN_IDS:
        if text.startswith("/add "):
            try:
                new_id = int(text.split()[1])
                allowed_users.add(new_id)
                await send_message(chat_id, f"✅ Пользователь {new_id} добавлен.")
            except:
                await send_message(chat_id, "Формат: /add 123456789")
            return

        if text.startswith("/remove "):
            try:
                rem_id = int(text.split()[1])
                allowed_users.discard(rem_id)
                await send_message(chat_id, f"❌ Пользователь {rem_id} удалён.")
            except:
                await send_message(chat_id, "Формат: /remove 123456789")
            return

        if text == "/list":
            if allowed_users:
                ids = "\n".join(str(i) for i in allowed_users)
                await send_message(chat_id, f"Пользователи с доступом:\n{ids}")
            else:
                await send_message(chat_id, "Список пуст.")
            return

    # Кнопка «Узнать мой ID»
    if text == "🆔 Узнать мой ID":
        await send_message(chat_id, f"Твой ID: {user_id}\n\nСкопируй и отправь Ле 👆")
        return

    # Кнопка «Проверить доступ»
    if text == "🔄 Проверить доступ":
        if user_id in allowed_users or user_id in ADMIN_IDS:
            await send_course(chat_id)
        else:
            await send_message(chat_id,
                "⏳ Тебя пока нет в списке.\n\n"
                "Убедись, что отправила свой ID Ле. Как только она добавит — нажми кнопку снова."
            )
        return

    # /start или первый заход
    if text == "/start" or chat_id not in started_chats:
        started_chats.add(chat_id)
        await show_start(chat_id, first_name, user_id)


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
