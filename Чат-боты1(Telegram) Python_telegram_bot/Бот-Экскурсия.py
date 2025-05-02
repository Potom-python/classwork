import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

BOT_TOKEN = '8190247622:AAH7oqGSnQy4xVmhJSuWvm44EZEuuDMrYyc'


async def start(update, context):
    await update.message.reply_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!')
    return await hall1(update, context)


async def hall1(update, context):
    message = update.message.text if update.message else ""

    if message == '2 зал':
        return await hall2(update, context)
    elif message == 'Exit':
        return await stop(update, context)

    reply_keyboard = [['2 зал', 'Exit']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('В данном зале представлены вазы', reply_markup=markup)
    return 1


async def hall2(update, context):
    message = update.message.text if update.message else ""

    if message == '3 зал':
        return await hall3(update, context)

    reply_keyboard = [['3 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('В данном зале представлены мумии', reply_markup=markup)
    return 2


async def hall3(update, context):
    message = update.message.text if update.message else ""

    if message == '1 зал':
        return await hall1(update, context)
    elif message == '4 зал':
        return await hall4(update, context)

    reply_keyboard = [['4 зал'], ['1 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('В данном зале представлено снаряжение', reply_markup=markup)
    return 3


async def hall4(update, context):
    message = update.message.text if update.message else ""

    if message == '1 зал':
        return await hall1(update, context)

    reply_keyboard = [['1 зал']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text('В данном зале представлена броня', reply_markup=markup)
    return 4


async def stop(update, context):
    await update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, hall1)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, hall2)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, hall3)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, hall4)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
