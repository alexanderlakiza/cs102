import telebot


access_token = '1024662102:AAGl8-cZSLGVL8ze9tB8slgMc_z1lxr7MSk'
telebot.apihelper.proxy = {'https': 'https://91.236.239.149:3128'}
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

