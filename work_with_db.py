import sqlite3
from Category import *

def create_database(categories):
	conn = sqlite3.connect('text.db')
	cursor = conn.cursor()
	script = ""
	for category in categories:
		script += 'INSERT INTO categories (name, url) VALUES ("{}", "https://lenta.ru/rubrics/{}");'.format(category, category)

	cursor.execute('DROP TABLE IF EXISTS textes;')
	cursor.execute('DROP TABLE IF EXISTS categories;')
	cursor.execute('''CREATE TABLE textes
		         (id integer primary key autoincrement,
		         category text,
		         txt text,
		         url text);''')
	cursor.execute('''CREATE TABLE categories
		         (id integer primary key autoincrement,
		         url text,
		         name text);''')
	cursor.executescript(script)
	conn.close()

def get_categories():
	conn = sqlite3.connect('text.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM categories')
	sql_categories = cursor.fetchall()
	conn.close()
	categories = []
	for sql_category in sql_categories:
		category = Category(id = sql_category[0], name = sql_category[2], url = sql_category[1])
		categories.append(category)
	return categories

def save_category(categories):
	conn = sqlite3.connect('text.db')
	cursor = conn.cursor()
	for category in categories:
		cursor.execute('UPDATE categories SET  = "{}" WHERE id = "{}";'.format(category.html, category.id))
	conn.close()

def save_articl(articl):
	conn = sqlite3.connect('text.db')
	cursor = conn.cursor()
	cursor.executescript('INSERT INTO textes (category, txt, url) VALUES ("{}", "{}", "{}");'.format(articl.category, articl.text, articl.url))
	conn.close()