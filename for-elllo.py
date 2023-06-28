import requests
from bs4 import BeautifulSoup

for num in range(901, 1000, 25):
    url = f'https://www.elllo.org/video/0{num}/index.htm'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = soup.find_all('div', class_='mobilelist')

    for i in quotes:
        i = str(i)
        print(i)
        print()

        # Название страницы (из ссылки на страницу)
        a = i.find('<a href="')
        b = i[a:].find('">')
        print(a)
        print(b + a)
        new = i[a:(b + a)]
        print(i[a:])
        print(new)

        new_url = url[:len(url) - 9] + new
        print(new_url)

        response = requests.get(new_url)
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            # Название видео
            name = soup.find('div', class_='video-question').text.strip()
            print(name)

            # Ссылка на видео Vimeo
            video_url = str(soup.find('iframe'))
            video_url = video_url[video_url.find('src="') + 5:video_url.find('" width=')]
            print(video_url)

            # Текст к видео (транскрипция)
            text = soup.find('div', class_='transcript').text.strip()
            text = ''.join(text.replace('\n', '!@#$'))
            text = text.replace('â', "'")
            text = text.replace('â¦', "...")
            print(text)

            js_url = str(soup.find_all('script', type='text/javascript'))
            js_url = js_url[js_url.find('../../quiz/') + 6:]
            js_url = 'https://www.elllo.org/' + js_url[:js_url.find('" type="text')]

            response = requests.get(js_url)
            soup = BeautifulSoup(response.text, 'lxml')

            quiz = soup.find('p').text
            quiz = ''.join(quiz.split('\n'))

            with open('801-900.txt', 'r+') as f:
                f.seek(0, 2)
                f.write(new)
                f.write('|')
                f.write(video_url)
                f.write('|')
                f.write(name)
                f.write('|')
                f.write(text)
                f.write('|')
                f.write(quiz)
                f.write('\n')

        except Exception as e:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', new_url)
