# Публикация комикс-картинок про Python на стену в группе ВКонтакте

Проект берет случайную комикс-картинку про Python с комментариями автора с сайта `https://xkcd.com/` и публикует ее на стену сообщества ВКонтакте

В проекте два рабочих файла:
- `comics_helper` - файл в котором находятся вспомогательные функции (скачивание картинки с интернта по заданной ссылке, создание url для запроса к API VK
по заданному методу запроса).
- `comics` - основной файл проекта. 

Для публикации картинки необходимо сделать следующие шаги:
- создать приложение для постинга в ВК
https://dev.vk.com/ - сайт для создания приложений ВК, тип указываем `standalone`
- получить `client_id` вашего приложения
нажать на кнопку “Редактировать” для нового приложения, в адресной строке вы увидите его client_id
- получить токен для приложения, которое будет выкладывать картинки
https://vk.com/dev/implicit_flow_user, использовать `Implicit Flow`, убрать параметр `redirect_uri` у запроса на ключ, scope=photos,group,swall,offline
- получить `client_id` группы, куда будут выкладываться картинки
https://regvk.com/id/ - Узнать ID страницы или группы ВКонтакте
- получить адреса для загрузки картинки
это делает функция `upload_picture_to_server`
- загрузить картинку на сервер
это делает функция `upload_picture_to_server`
- сохранить картинку в альбоме группы
это делает функция `upload_picture_to_album`
- публикация записи в группе
это делает функция `post_picture_to_wall`
в этой функции есть параметры запроса:
```py
    post_picture_payload = {'from_group': 1,           # 1 - сообщение от имени группы, 0 - от имени пользователя
                            'message': comics_comment, # комментарий со страницы xkcd комикса
                            }

```

В процессе работы программа будет создавать картинку `comics.jpg` в папке с запущенной программой, туда будет записываться скаченный комикс. 
После завершения выполнения программы картинка будет автоматически удалена

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```
- Для работы программы необходимо VK_ACCESS_TOKEN, VK_GROUP_ID. Как их получить описано выше.
- Создать в корневом катологе файл .env
- Записать в этом файле полученные `VK_ACCESS_TOKEN`, `VK_GROUP_ID`.

``` 
VK_ACCESS_TOKEN=...............................
VK_GROUP_ID=...............................
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
