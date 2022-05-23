import time
import telebot
import requests
import os

token = '5390348958:AAEwy_3Dh-J8jgTjBUqfHOTvjwqe8horK6s'
bot = telebot.TeleBot(token)
directoryName = "telegram_data"
os.chdir(directoryName)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Здравствуйте! Отправьте аудиосообщение!</b>', parse_mode='html')

@bot.message_handler(content_types=['voice'])
def repeat_all_message(message):
    start_time = time.process_time()
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    user_id = message.from_user.id
    if not os.path.isdir(str(user_id)):
        os.mkdir(str(user_id))

    with open(f'{user_id}/{message.message_id}.ogg', 'wb') as f:
        f.write(file.content)
    #res = requests.post(url="http://127.0.0.1:3001/api/translate_q/1")
    print(str(time.process_time() - start_time) + " секунд")


bot.polling(none_stop=True)
