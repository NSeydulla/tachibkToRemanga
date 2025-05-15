# TACHIBK > Remanga

### Требования:

- [Python](https://python.org) 3.x and depencencies:
  - `pip install -r requirements.txt`

##

### Что она делает:

Добавит все тайтлы с tachiyomi в закладки  
Проставит лайки и просмотры всем главам которые вы смотрели в tachiyomi

##

### Как пользоваться:

- Конвертировать бэкап файл в json
  - Перейти по [Ссылка](https://github.com/BrutuZ/tachibk-converter/tree/main) и сконвертировать tachibk файл в json
  - Переименовать json файл в "data.json"
  - Закинуть его в одну директорию с main.py
- Получить токен авторизации
  - Открыть в браузере ремангу
  - Нажать ctrl+shift+c
  - Открыть вкладку Network
  - Перезагрузить страницу
  - Поставить фильтр если нужно
  - Открыть любой запрос на сервер апи реманги
  - Скопировать Токен
  - Вставить его в main.py
![Screenshot](/image.png)
- Настроить словарь "CategoryToBookmark" под себя
  - Узнать какой "order" у категории можно в файле "data.json"
- Запустить код
  - `py main.py`
