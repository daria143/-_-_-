import telebot
import requests
import time

token = '5353254615:AAEfV22Vb0Gv3Nb-q17z4A-tXh-zJiyXpsI'
bot = telebot.TeleBot(token)
error_message = "<b>Введите id пользователя и id сообщения через пробел!</b>"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Здравствуйте! Введите id пользователя и id сообщения через пробел!</b>',
                     parse_mode='html')

@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    start_time = time.process_time()
    data_message = str(message.text).split(" ")
    if len(data_message)!=2:
        bot.send_message(message.chat.id, error_message, parse_mode='html')
    elif not data_message[0].isdigit() or not data_message[1].isdigit():
        bot.send_message(message.chat.id, '<b>id это число</b>', parse_mode='html')
    else:
        res = requests.get(url="http://127.0.0.1:3002/api/found/" + str(data_message[0]) + "/" + str(data_message[1]))
        if res.status_code != 200:
            bot.send_message(message.chat.id, '<b>Не удалось найти сообщение или пользователя</b>', parse_mode='html')
        else:

            answer = ''
            result = res.json()
            notfound = False
            for i in range(len(result)):
                currentRow = result[str(i)]
                sub_name = currentRow[2]['sub_name']
                name = currentRow[0]['name']
                value = currentRow[1]['value']
                if sub_name != "" and value != "":
                    answer = answer + f'<b>Продукт: {sub_name} {name}: {value}</b>\n'
                elif sub_name != "" and value == "":
                    answer = answer + f'<b>Вид продукта: {sub_name} Продукт: {name}</b>\n'
                else:
                    notfound = True
                    answer = answer + f'<b>{name}</b>\n'

            if notfound:
                answer = "<b>По запросу ничего не найдено, скажите, какой вид продукции из списка ниже вас интересует:</b>\n" + answer

            bot.send_message(message.chat.id, answer, parse_mode='html')
            print(str(time.process_time() - start_time) + " секунд")






bot.polling(none_stop=True)
