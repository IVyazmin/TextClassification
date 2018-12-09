import work_with_db
import work_with_site
from Articl import *

categories_names = ['economics', 'science', 'culture', 'sport', 'travel']

def find_articls_urls(categories):
	articls = []
	for category in categories:
		html = category.html
		while True:
			index_div = html.find('<div class="item news b-tabloid__topic_news">')
			if index_div == -1:
				break
			string_with_link = html[index_div:]
			link_start = string_with_link.find('<a href=')
			link_end = string_with_link.find('>', link_start)
			string_with_url = string_with_link[link_start:link_end]
			url_start = string_with_url.find('"') + 1
			url_end = string_with_url.rfind('"')
			url = 'https://lenta.ru' + string_with_url[url_start:url_end]
			articl = Articl(url = url, category = category.name)
			articls.append(articl)
			html = html[index_div + 5:]
	return articls


def get_text_from_articl(html):

	def get_p_from_div(text):
		array_of_p = []
		while True:
			index_start = text.find('<p>')
			if index_start == -1:
				break
			index_end = text.find('</p>', index_start)
			p_string = text[index_start + 3:index_end]
			array_of_p.append(p_string)
			text = text[index_end:]
	
		return array_of_p
	
	def get_text_from_p(text):
	
		while True:
			index_start = text.find('<')
			if index_start == -1:
				break
			index_end = text.find('>')
			text = text[:index_start] + text[index_end + 1:]
	
		while True:
			index_cov = text.find("'")
			if index_cov == -1:
				break
			text = text[:index_cov] + text[index_cov + 1:]

		while True:
			index_cov = text.find('"')
			if index_cov == -1:
				break
			text = text[:index_cov] + text[index_cov + 1:]

		return text
	
	
	def get_div_from_html(text):
		index_start = text.find('itemprop="articleBody"')
		index_end = text.find('itemprop="author"', index_start)
		div_text = text[index_start:index_end]
	
		return div_text
	
	div = get_div_from_html(html)
	ps = get_p_from_div(div)
	text = ''
	for p in ps:
		p_text = get_text_from_p(p)
		text += p_text
	return text
	

def create_data():
	work_with_db.create_database(categories_names)
	categories = work_with_db.get_categories()
	for category in categories:
		category.html = work_with_site.get_html(category.url)
	articls = find_articls_urls(categories)
	for articl in articls:
		articl.html = work_with_site.get_html(articl.url)
		articl.text = get_text_from_articl(articl.html)
		work_with_db.save_articl(articl)

create_data()