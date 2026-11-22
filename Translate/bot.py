import telebot
from translate import translate

bot = telebot.TeleBot("9245231999:AAEduY9cR4f5oPNj5_QC-VsdS5-FZRkPHIA")

@bot.message_handler(commands=["ni", "translate"])
def echo_all(message):
    translated_text: str = translate(' '.join(message.text.split(' ')[1:]))
    if not translated_text:
        bot.reply_to(message, "![This text cannot be translated]")
        return
    bot.reply_to(message, translated_text)

bot.infinity_polling()