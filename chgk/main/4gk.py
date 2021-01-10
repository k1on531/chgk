import requests
import re

URL = 'https://db.chgk.info'
PAGE = '/last?page='
TOUR_URL = 'tour/'
pattern = re.compile(r'<td><a href="(.*?)".*?</a>')


def get_urls(page=None):
	url = URL
	if page != None:
		url += PAGE + str(page)
	r = requests.get(url)
	urls = re.findall(pattern, r.text)
	return urls


def get_questions(tour_name):
	r = requests.get(URL + tour_name)
	p = r'<div class="question".*>(.*)<\/div>'
	res = re.findall(r'<div class="question"(.*?)>(Вопрос \d+)<\/a>:<\/strong> (.*?)<\/p>.*?<strong class="Answer">(Ответ:)</strong>(.*?)</p>.*?<strong class="Comments">(Комментарий:)</strong>(.*?)</p>.*?<strong class="Authors">(Автор:)</strong>.*?>(.*?)</a>.*?<\/div>', r.text, flags=re.DOTALL)
	result = []
	for i in res:
		if i[2].startswith('<div'):
			continue
		result.append({
			'question_number': i[1],
			'question_text': i[2].replace('&nbsp;', '').replace('<br />\n', ''),
			'answer': i[4],
			'comment': i[6],
			'author': i[8],
			})
	return result


def main():
	r = requests.get(URL)
	urls = get_urls()
	pages_count_pattern = re.compile(r'<a href="/last\?page=(\d+?)" title="Перейти на последнюю страницу"')
	pages_count = int(re.search(pages_count_pattern, r.text).group(1))
	print(f'Pages: {pages_count}')
	for i in range(1, 2):
		current_urls = get_urls(i)
		urls += current_urls
	print(urls)
	questions = []
	for i in urls:
		questions += get_questions(i)
	for i in questions:
		print(i['question_number'] + ':' + i['question_text'])
		print('Ответ:' + i['answer'])
		print('Автор: ' + i['author'])
		print('\n-----\n')


if __name__ == '__main__':
	main()
