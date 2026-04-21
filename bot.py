import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "8614216581:AAEzpGkNOPtgQABf_mqXcjrAWM_RDT1Bpy8")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # твой Telegram ID

# Здесь будут file_id видео — заполним после загрузки
VIDEOS = [
    # {"title": "Урок 1 — Танец", "file_id": "BAACAgI..."},
    # {"title": "Урок 2 — Танец", "file_id": "BAACAgI..."},
]

# Пользователи с доступом (хранится в памяти, после перезапуска сбрасывается)
# Для продакшна потом заменим на файл или базу
paid_users = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id in paid_users:
        await send_course(update, context)
        return

    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Это курс Ле — танец, философия и мудры в одном путешествии.\n\n"
        "💳 Стоимость: *XXXX₽*\n"
        "Реквизиты для оплаты: *XXXX*\n\n"
        "После оплаты напиши сюда свой *ID*: `" + str(user_id) + "`\n"
        "И я открою тебе доступ к курсу ✨"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def send_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Доступ открыт! Отправляю материалы курса...\n\n"
        "Сохрани этот чат — здесь все уроки 🙏"
    )

    if not VIDEOS:
        await update.message.reply_text(
            "⏳ Видео ещё загружаются, скоро всё будет здесь!"
        )
        return

    for video in VIDEOS:
        await update.message.reply_video(
            video=video["file_id"],
            caption=f"*{video['title']}*",
            parse_mode="Markdown"
        )


# Команда для админа: /give USER_ID
async def give_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Используй: /give USER_ID")
        return

    try:
        user_id = int(context.args[0])
        paid_users.add(user_id)
        await update.message.reply_text(f"✅ Доступ выдан пользователю {user_id}")

        # Уведомляем пользователя
        await context.bot.send_message(
            chat_id=user_id,
            text="🎉 Оплата получена! Напиши /start чтобы получить курс"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


# Команда /myid — чтобы узнать свой ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Твой ID: `{update.effective_user.id}`", parse_mode="Markdown")


# Команда /addvideo — бот пришлёт file_id загруженного видео
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    video = update.message.video or update.message.document
    if video:
        file_id = video.file_id
        await update.message.reply_text(
            f"✅ file\\_id получен:\n`{file_id}`",
            parse_mode="Markdown"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("give", give_access))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

    logger.info("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
