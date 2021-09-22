from pyowm import OWM
from pyowm.utils.config import get_default_config
import telebot

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('1298f2e11dad29efed901455a5660c4e', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot("1976342692:AAFB6TAywnb4s5LVI1SQk9CdZol5S_VrG9M")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    detailed_status = w.detailed_status
    wind = w.wind()["speed"]

    answer = "В городе " + message.text + " сейчас " + detailed_status + "\n"
    answer += "Температура: " + str(temperature) + " \u2103" + "\n"
    answer += "Ветер: " + str(wind) + " м/с " + "\n"

    if temperature < 10:
        answer += "Сейчас, очень холодно, одевайся, как можно теплее"
    elif temperature < 15:
        answer += "Сейчас, прохладно, но все же одевайся тепло"
    elif temperature < 20:
        answer += "Сейчас, прохладно, но, можешь сильно не укутываться, не замерзнешь)"
    else:
        answer += "На улице тепло, одевайся как пожелаешь"

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
