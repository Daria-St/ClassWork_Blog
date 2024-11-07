import requests
import telebot

token = '7362413029:AAHHnVzlmGhOlwldW2OWRjR1JRErFPEqH1M'

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'привет')

bot.infinity_polling()

# url = f"https://api.telegram.org/bot{token}/getMe"
# # res = requests.get(url)
# # print(res.json())
#
# url_updates = f"https://api.telegram.org/bot{token}/getUpdates"
# # res = requests.get(url_updates)
# # print(res.json())
#
#
# user_id = 398923180
# url_send = f"https://api.telegram.org/bot{token}/sendMessage"
# res = requests.get(url_send, data={"chat_id":user_id, 'text':'упс'})

