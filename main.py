import json
import requests
import enum
import re

authorization = "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

class BookMarks(enum.Enum): # Закладки в remanga и их айдишки
    reading = 1 # Читаю
    will_read = 2 # Буду читать
    readed = 3 # Прочитано
    abandoned = 4 # Брошено
    postponed = 5 # Отложено
    not_interested = 6 # Не интересно
    # Сюда можно добавить закладку которую ты сам создал

    # Узнать id своей закладки
    # https://api.remanga.org/api/v2/users/ID_АККАУНТА/user_bookmarks/
    
    # Узнать id своего аккаунта
    # https://api.remanga.org/api/v2/users/current/

CategoryToBookmark = { # order категории
    None: BookMarks.will_read,
    "0": BookMarks.reading,
    "1": BookMarks.reading,
    "2": BookMarks.reading,
    "3": BookMarks.reading,
    "4": BookMarks.reading,
    "5": BookMarks.reading,
    "6": BookMarks.not_interested
}

# Исправь под свой список категории
# Например у меня был такой список категории
# {'name': 'Смотрю', 'id': '1', 'flags': '28'}
# {'name': 'Онгоинг', 'order': '1', 'id': '2', 'flags': '28'}

# Смотрю(order - 0) и Онгоинг(order - 1) у меня идет в Читаю
# Дефолт категория(order - None) идет в Буду читать

# Order можно узнать запустив код ниже

# with open('data.json', 'r', encoding='utf-8') as file:
#     data = json.loads(file.read())
# for backupCategory in data['backupCategories']:
#     print(backupCategory)
# exit()


session = requests.Session()
session.headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "authorization": authorization,
    "content-type": "application/json"
}

if not session.get("https://api.remanga.org/api/v2/users/current/").ok:
    print('Не введен или не правильный токен авторизации!')
    exit()

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())

sourceId = '' # должно быть "8983242087533137528", но мб не у всех
for backupSource in data['backupSources']:
    if backupSource['name'] == 'Remanga':
        sourceId = backupSource['sourceId']
        break

if sourceId == '':
    print("Не найден источник remanga")
    exit()

p = re.compile(r"(\d+)$")
for backupManga in data['backupManga']:
    if backupManga['source'] != sourceId:
        continue
    print(f"---\n\n{backupManga['title']}\n")

    bookmark = CategoryToBookmark.get(backupManga.get('categories', [None])[0])
    if bookmark is None:
        print(f'Не прописана закладка для категории с id - {backupManga['categories'][0]}\n')
        continue

    for sequence in backupManga['url'].split('/')[::-1]:
        if len(sequence) != 0:
            url = sequence
            break

    title_response = session.get(f"https://api.remanga.org/api/v2/titles/{url}")
    if not title_response.ok:
        print(f"Ошибка, либо тайтла нет, либо еще что-то")
        print(title_response.text)
        print(backupManga.get('description', "Нет описания"))
        continue

    chapters_ids = []
    for chapter in backupManga['chapters']:
        if chapter.get('read',False):
            chapters_ids.append(int(p.search(chapter['url']).group(1)))

    r = session.post(f'https://api.remanga.org/api/activity/views/', json={"chapter_ids": chapters_ids})
    if not r.ok:
        print(f"Что то не так!\n{r}\n{r.text}\n")

    r = session.post(f'https://api.remanga.org/api/activity/votes/', json={"chapter_ids": chapters_ids})
    if not r.ok:
        print(f"Что то не так!\n{r}\n{r.text}\n")

    title_data = title_response.json()
    if title_data['bookmark_type'] == bookmark.value:
        # print("Уже находится в нужной закладке")
        continue

    bookmark_response = session.post('https://api.remanga.org/api/users/bookmarks/', json={"title":title_data["id"],"type":bookmark.value})
    if not bookmark_response.ok:
        print(f"Ошибка с изменением закладки у тайтла")
        print(bookmark_response.text)