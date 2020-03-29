from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import messagequeue as mq

from handlers import *
from settings import *

log = logging.getLogger()
log.setLevel(logging.INFO)
# handler = logging.FileHandler('bot.log', 'w', 'utf-8')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def my_test(context):
    """Testing the job"""
    print('Тest')
    context.bot.send_message(chat_id='409569568',
                             text='One message every minute')
    context.job.interval += 5
    if context.job.interval > 15:
        context.bot.send_message(chat_id='409569568',
                                 text='No more spam for you!')
        context.job.schedule_removal()


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY, use_context=True)

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    # mybot.job_queue.run_repeating(my_test, interval=5, first=0)
    mybot.job_queue.run_repeating(send_updates, 5)

    anketa = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)],
        states={
            'name': [MessageHandler(Filters.text, anketa_get_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            'comment': [CommandHandler('skip', anketa_skip_comment),
                        MessageHandler(Filters.text, anketa_comment),
                        ]
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document,
            dontknow
        )]
    )

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('pic', send_pic))
    dp.add_handler(CommandHandler('userinfo', userinfo))
    dp.add_handler(CommandHandler('caps', caps))
    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_pic))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить смайлик)$'), change_user_emo))
    dp.add_handler(MessageHandler(Filters.contact, get_contact))
    dp.add_handler(MessageHandler(Filters.location, get_location))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(MessageHandler(Filters.photo, describe_photo))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
