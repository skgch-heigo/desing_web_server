import logging
import aiohttp

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config.config import BOT_TOKEN, SITE_URL, LOG_FILE, LOG_LEVEL

# Запускаем логгирование
from data.constants.tables_inf import TABLES_CLASSES, RELATIONS, FIELDS
from data.models import db_session

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOG_LEVEL, filename=LOG_FILE
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    if update.message.text.lower() == "Give battle advice".lower():
        await update.message.reply_text("Go for the eyes!")
    else:
        await update.message.reply_text("I'm sorry, currently I don't support texting, so please use only commands.")


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    reply_keyboard = [['/get Hats', '/get Boots'],
                      ['/get Lower_body', '/get Upper_body']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}! I'm Wilson. I can help you accessing Design Helper", reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("""Possibe commands:
    /start
    /get <table>    -  to get data from table""")


async def get_response(url, params=None):
    if params is None:
        params = {}
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def get_data(update, context):
    response = await get_response(SITE_URL + "/api/" + context.args[0].lower())
    answer = ""
    table = TABLES_CLASSES[context.args[0]]
    db_sess = db_session.create_session()
    print(response)
    for i in response:
        for j in response[i]:
            for k in FIELDS[context.args[0]][1:-1]:
                if k in RELATIONS:
                    name = db_sess.query(TABLES_CLASSES[RELATIONS[k]]).filter(TABLES_CLASSES[RELATIONS[k]].id
                                                                              == j[k]).first()
                    if name:
                        name = name.name
                    else:
                        name = ""
                    answer += str(k) + ": " + name + "\n"
                else:
                    answer += str(k) + ": " + str(j[k]) + "\n"
            answer += "\n"
        answer += "\n\n"
    answer = answer.strip()
    await update.message.reply_text(answer)


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    db_session.global_init("db/designer_base.db")

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get", get_data))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()