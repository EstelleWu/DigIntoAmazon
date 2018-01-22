# strategy

# soup --> table id = 'productDetailsTable'
# 		 find_all li tag --> get 4th li
# 	   --> Detail --> iframe div.text

from bs4 import BeautifulSoup
from selenium import webdriver


class Book():
	"""docstring for Book"""
	def __init__(self):
		self.title = ""
		self.link = ""
		self.isbn = ""
		self.des = ""
		self.summary = ""

def get_book_list():

	driver = webdriver.PhantomJS(executable_path = '/Users/wuyu/Desktop/projects/web_spider/phantomjs-2.1.1-macosx 2/bin/phantomjs')

	url = 'https://www.amazon.com/s/ref=nb_sb_ss_c_1_7?url=search-alias%3Daps&field-keywords=python+programming&sprefix=python+%2Caps%2C581&crid=Q13RO8S4RT5E'

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'lxml')

	ul = soup.find('ul', {'id': 's-results-list-atf'})

	book_list = []

	for li in ul.find_all('li', class_ = 's-result-item celwidget '):
		all_a = li.find_all('a')
		#the second
		#open all the div beforehand to know the order of this a_tag
		# print all_a[1].text
		# print all_a[1]['href']

		new_book = Book()
		new_book.title = all_a[1].text
		new_book.link = all_a[1]['href']
		book_list.append(new_book)

	driver.quit

	return book_list

def get_detail_book_list(book_list):

	driver = webdriver.PhantomJS(executable_path = '/Users/wuyu/Desktop/projects/web_spider/phantomjs-2.1.1-macosx 2/bin/phantomjs')

	for b in book_list[0:2]:


		#url = 'https://www.amazon.com/Python-Programming-Introduction-Computer-Science/dp/1590282418/ref=sr_1_4?ie=UTF8&qid=1494029893&sr=8-4&keywords=python+programming'
		url = b.link

		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		table = soup.find('table', {'id': 'productDetailsTable'})

		all_li = table.find_all('li')

		isbn = all_li[3].text.strip('ISBN-10: ')
		b.isbn = isbn

		#print isbn
		#--------------------------------------------

		# bc switch to another html!!!
		driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
		soup = BeautifulSoup(driver.page_source, 'lxml')

		description = soup.find('div').text
		print description
		b.des = description


	driver.quit()

#get_detail_book_list(get_book_list())


def get_top_comment(book_list):

	driver = webdriver.PhantomJS(executable_path = '/Users/wuyu/Desktop/projects/web_spider/phantomjs-2.1.1-macosx 2/bin/phantomjs')

	#url = 'https://www.amazon.com/Python-Programming-Introduction-Computer-Science/dp/1590282418/ref=sr_1_4?ie=UTF8&qid=1494029893&sr=8-4&keywords=python+programming'

	for b in book_list[0:2]:

		url = b.link

		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		#summary
		div = soup.find('div', {'id': 'reviewsMedley'}) 

		summary = div.find('a', {'class': 'a-link-normal a-text-normal'})

		b.summary = summary['title']

		print b.summary


		#top customer reviews
		divv = soup.find('div', {'id': 'cm-cr-dp-review-list'})

		all_r = divv.find_all('div', {'data-hook': 'review'})

		for r in all_r:
			rev = r.find('a', {'data-hook': 'review-title'})
			review = rev.text
			print review

		print '\n'
	

	driver.quit



#print get_book_list
#print get_top_comment(get_book_list())
print get_detail_book_list(get_book_list) 












