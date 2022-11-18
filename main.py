import config, database, models

import telebot, sqlite3

from telebot import types
from models import *

bot = telebot.TeleBot(config.TOKEN)
ref_link = 'https://telegram.me/{}?start={}'

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn = types.KeyboardButton('✅ Клик')
	btn2 = types.KeyboardButton('👀 Профиль')
	btn3 = types.KeyboardButton('💸 Смотреть рекламу')
	markup.add(btn, btn2, btn3)

	user_id = message.chat.id
	splited = message.text.split()
	if not Users.user_exists(user_id):
		Users.create_user(user_id)
		if len(splited) == 2:
			Users.increase_ref_count(splited[1])

	if database.check(message) == False:

		database.main(message)
		bot.reply_to(message, """
Привет❤\n\n💸 *Зарабатывай* кликая на кнопку или *смотря рекламу!*
""", parse_mode='Markdown', reply_markup=markup)
	else:
		bot.reply_to(message, """
Привет❤\n\n💸 *Зарабатывай* кликая на кнопку *или смотря рекламу!*
""", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler()
def message(message):
	if message.text == '✅ Клик':
		database.click(message)
	if message.text == '👀 Профиль':
		profile(message)
	if message.text == '💸 Смотреть рекламу':
		bot.reply_to(message, '❌Команда больше не доступна❗')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == 'ref':
			count = Users.get_ref_count(call.message.chat.id)
			bot_name = bot.get_me().username

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{call.message.chat.username}

Рефералов - {count}

Ваша реферальная ссылка
`{ref_link.format(bot_name, call.message.chat.id)}`
''', parse_mode='Markdown''')
			

def profile(message):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton('Мои рефералы', callback_data='ref')
	markup.add(btn1)

	bot.reply_to(message, f"""
{message.chat.username}

Баланс - {database.profile(message)[1]}
""", parse_mode="Markdown", reply_markup=markup)

def send_database(message, text):
	bot.send_message(message, text)

if __name__ == '__main__':	
	bot.infinity_polling()
	