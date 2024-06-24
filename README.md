# -- > API Сервис для сбора отзывов < --

### Общее описание
Сервис собирает отзывы пользователей на произведения. Сами произведения в сервисе не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Ресурсы API сервиса
* Ресурс auth: аутентификация.

* Ресурс users: пользователи.

* Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

* Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.

* Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

* Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.

* Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

### Пользовательские роли и права доступа
* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Подготовка проекта к запуску под Linux

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:PetrovKRS/reviews-service.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Документация к API:

```
http://127.0.0.1:8000/redoc/
```

### Самостоятельная регистрация новых пользователей
* Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
* Сервис отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт     
  /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).

В корне проекта необходимо создать файл .env со следующими переменными окружения:
* EMAIL_HOST = smtp.mail_server
* EMAIL_HOST_USER = your_mail@mail_server
* EMAIL_HOST_PASSWORD = *****************
* EMAIL_PORT = smtp порт вашего mail сервера
* EMAIL_USE_SSL = True

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.

После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

Стек технологий:| Python 3.9 | Django REST Framework | SQLite3 | 


### Работа была выполнена в рамках группового проекта, командой из 3-х человек:

 |*| [Андрей Петров](https://github.com/PetrovKRS) |*| [Артем Волобуев](https://github.com/v-artem) |*| [Дмитрий Сайранов](https://github.com/Vergil-KOD) |*|
