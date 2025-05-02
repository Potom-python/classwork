# Импортируем необходимые классы.
import logging
from random import randint

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler

BOT_TOKEN = '7742478380:AAGahc02v2Nb3q3uNIw2MnXJ6XyxeS5MMfM'

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
async def set_timer(update, context):
    text = update.message.text
    if text == '30 секунд,':
        TIMER = 30
    elif text == '1 минута,':
        TIMER = 60
    elif text == '5 минут,':
        TIMER = 5 * 60
    elif text == 'вернуться назад.':
        reply_keyboard = [['/dice', '/timer']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            'Главное меню:',
            reply_markup=markup
        )
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'засек {TIMER}с'
    reply_keyboard = [['/close']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text, reply_markup=markup)


async def task(context):
    """Выводит сообщение"""
    reply_keyboard = [['30 секунд,'], ['1 минута,'],
                      ['5 минут,'], ['вернуться назад.']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await context.bot.send_message(context.job.chat_id, text=f'истекло {context.job.data}', reply_markup=markup)


async def start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        'Главное меню',
        reply_markup=markup
    )


async def dice(update, context):
    reply_keyboard = [['кинуть один шестигранный кубик,'], ['кинуть 2 шестигранных кубика одновременно,'],
                      ['кинуть 20-гранный кубик,'], ['вернуться назад.']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        'Выберите кубик:',
        reply_markup=markup
    )


async def timer(update, context):
    reply_keyboard = [['30 секунд,'], ['1 минута,'],
                      ['5 минут,'], ['вернуться назад.']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        'Выберите время:',
        reply_markup=markup
    )


async def roll_dice(update, cotext):
    text = update.message.text
    if text == 'кинуть один шестигранный кубик,':
        await update.message.reply_text(f'{randint(1, 6)}')
    elif text == 'кинуть 2 шестигранных кубика одновременно,':
        await update.message.reply_text(f'{randint(1, 6)} {randint(1, 6)}')
    elif text == 'кинуть 20-гранный кубик,':
        await update.message.reply_text(f'{randint(1, 20)}')
    elif text == 'вернуться назад.':
        reply_keyboard = [['/dice', '/timer']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            'Главное меню:',
            reply_markup=markup
        )


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    reply_keyboard = [['30 секунд,'], ['1 минута,'],
                      ['5 минут,'], ['вернуться назад.']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(text, reply_markup=markup)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler('timer', timer))
    application.add_handler(CommandHandler("close", unset))
    application.add_handler(MessageHandler(filters.Regex(
        '^(кинуть один шестигранный кубик,|кинуть 2 шестигранных кубика одновременно,'
        '|кинуть 20-гранный кубик,|вернуться назад.)$'),
        roll_dice))
    application.add_handler(
        MessageHandler(filters.Regex('^(30 секунд,|1 минута,|5 минут,|вернуться назад.)$'), set_timer))

    application.run_polling()


if __name__ == '__main__':
    main()
