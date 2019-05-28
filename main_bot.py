import config
import telebot
import schedule
import time
import logging

from DB_wrapper import DBWrapper

MINUTES_TO_REPEAT = 1

bot = telebot.TeleBot(config.token)
db = DBWrapper(config.db_connection)
logging.basicConfig(filename="log.log", level=logging.ERROR)


def show_table_sizes(user_id):
    data = db.get_tables_sizes()
    bot.send_message(user_id, data)


def notifications(user_id):
    schedule.every(MINUTES_TO_REPEAT).minutes.do(show_table_sizes, user_id)
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(func=lambda m: True)
def stop(message):
    msg = "Hello! Please, wait {} minutes to get tables' sizes".format(MINUTES_TO_REPEAT)
    bot.send_message(message.chat.id, msg)
    user_id = message.chat.id
    notifications(user_id)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(e)
            time.sleep(15)
