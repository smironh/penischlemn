import main
from main import bot

import sqlite3

def check(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('''CREATE TABLE IF NOT EXISTS user(
ID INT,
balance INT default(0)
)''')

		cursor.execute('SELECT ID FROM user WHERE ID=?', (message.chat.id, ))
		info = cursor.fetchone()
		if info is None:
			return False
		else:
			return 'penis'
def main(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('''CREATE TABLE IF NOT EXISTS user(
ID INT,
balance INT default(0)
)''')

		cursor.execute('INSERT INTO user(ID) VALUES(?)', (message.chat.id, ))
def profile(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('SELECT * FROM user WHERE ID=?', (message.chat.id, ))
		info = cursor.fetchone()

		return info
		
def click(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('UPDATE user SET balance = balance + 1 WHERE ID=?', (message.chat.id, ))
		bot.send_message(message.chat.id, '+1 Монет💸')