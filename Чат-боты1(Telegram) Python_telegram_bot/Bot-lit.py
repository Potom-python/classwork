from telegram.ext import Application

BOT_TOKEN = '1'
stix = {1: 'Я помню чудное мгновенье:', 2: 'Передо мной явилась ты,',
        3: 'Как мимолетное виденье,', 4: 'Как гений чистой красоты.'}
cur = 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.run_polling()


if __name__ == '__main__':
    main()
