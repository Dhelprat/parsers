import requests
from bs4 import BeautifulSoup
from telegraph import Telegraph
import time as t

for num in range(1, 11):
    url = 'https://www.gastronom.ru/recipe/group/1132/recepty-napitkov-domashnie-napitki?page='
    url += str(num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = soup.find_all('article', class_='material-anons col-sm-4 col-ms-12')


    def send_telegram(text: str):
        token = "5389441275:AAG8KUqkYWIVU054GKupTQUDbjPABOLjWtI"
        url = "https://api.telegram.org/bot"
        channel_id = "@DelayedCookMeRecipes"
        url += token
        method = url + "/sendMessage"

        requests.post(method, data={
            "chat_id": channel_id,
            "text": text,
            "parse_mode": 'Markdown'
        })


    for i in quotes:
        try:
            type_recipe = '#Напитки'
            quote = i.find_all('a', class_='material-anons__like-ico')
            quote = str(quote[0])
            new_url = 'https://www.gastronom.ru' + quote[quote.find('href') + 6:quote.find('"></a>')]
            print(new_url)

            response = requests.get(new_url)
            soup = BeautifulSoup(response.text, 'lxml')

            name = soup.find('h1', class_='recipe__title').text
            if 'плов' in name.lower():
                continue

            try:
                description = soup.find('div', class_='recipe__intro').text
            except Exception:
                description = ''

            main_image = str(soup.find('img', class_='main-slider__image-image result-photo'))
            main_image = 'https://www.gastronom.ru' + main_image[main_image.find('src="') + 5:main_image.find('" title')]

            ingredients = []
            for ingredient in soup.find_all('li', class_='recipe__ingredient'):
                ingredients.append(ingredient.text)

            steps = []
            for step in soup.find_all('div', class_='recipe__step'):
                steps.append(step.find('div', class_='recipe__step-text').text.strip())

            time = soup.find_all('div', class_='recipe__summary-list-des recipe__summary-list-des_big')[-1].text

            count = soup.find('div', class_='recipe__summary-list-des', itemprop="recipeYield").text

            try:
                calories = soup.find('div', itemprop="calories").text.strip()
                protein_content = soup.find('div', itemprop="proteinContent").text.strip()
                fat_content = soup.find('div', itemprop="fatContent").text.strip()
                carbohydrate_content = soup.find('div', itemprop="carbohydrateContent").text.strip()
            except Exception:
                calories, protein_content, fat_content, carbohydrate_content = '-', '-', '-', '-'

            recipe = {
                'Название': name,
                'Картинка': main_image,
                'Описание': description.strip(),
                'Ингредиенты': ingredients,
                'Шаги': steps,
                'Время приготовления': time,
                'Количество порций': count,
                'Количество калорий': calories,
                'Белки': protein_content,
                'Жиры': fat_content,
                'Углеводы': carbohydrate_content
            }

            print(recipe)

            telegraph = Telegraph('f07a74ffd358a2f7b1487d02bc2f5bb71ab174c7461758fc1f538867f67d')

            result = telegraph.create_account(short_name='lalala')

            response = telegraph.create_page(
                recipe.get('Название'),
                author_name='Приготовь меня | Рецепты',
                author_url='https://t.me/CookMeRecipes',
                html_content=f"<p>{recipe.get('Описание')}</p><p><pre>Количество порций: {recipe.get('Количество порций')}</pre></p><p><pre>Время приготовления: {recipe.get('Время приготовления')}</pre></p>"
                             f"<img src='{recipe.get('Картинка')}'>"
                             f"<p><pre>КБЖУ: {recipe.get('Количество калорий')} | {recipe.get('Белки')} | {recipe.get('Жиры')} | {recipe.get('Углеводы')}</pre></p>"
                             f"<p><strong>Ингредиенты:</strong></p><ul>{''.join([f'<li>{i}</li>' for i in recipe.get('Ингредиенты')])}</ul>"
                             f"<p><strong>Пошаговый рецепт приготовления:</strong></p><p>{''.join([f'<p><strong>Шаг ' + str(recipe.get('Шаги').index(i) + 1) + '</strong></p><p>' + str(i) + '</p>' for i in recipe.get('Шаги')])}</p>"
                             f"<p><strong>Приятного аппетита!</strong></p>"
            )

            print('https://telegra.ph/{}'.format(response['path']))

            send_telegram("⚡️[" + recipe.get('Название') + "](https://telegra.ph/{})\n".format(response['path']) + type_recipe)

        except Exception:
            pass

        t.sleep(2)
