# Импортируем необходимые классы.
import asyncio
import datetime
import logging

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler

BOT_TOKEN = '7415428461:AAHXGdPO5IZ9kz1Eh71AAoH5uK-U3GUJPL0'

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TIMER = 5  # таймер на 5 секунд


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
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Вернусь через 5 с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! 5c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def echo(update, context):
    await update.message.reply_text(f'{update.message.text}')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def time(update, context):
    await update.message.reply_text(f'{datetime.datetime.now().time()}')


async def date(update, context):
    await update.message.reply_text(f'{datetime.datetime.now().date()}')


async def timer(update, context):
    if context.args:
        await update.message.reply_text('Таймер запущен')
        await asyncio.sleep(int(context.args[0]))
        await update.message.reply_text('Таймер сработал')
    else:
        await update.message.reply_text(
            'Напишите время через которое должен сработать таймер через пробел после /set_timer')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler('time', time))
    application.add_handler(CommandHandler('set_timer', timer))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler('date', date))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
