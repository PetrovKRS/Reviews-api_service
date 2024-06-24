import csv

from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Genre, Title, GenreTitle, Review, Comment
)
from users.models import User

# Важен порядок загрузки, чтобы соблюдались связи в таблицах!!!
CSV_BASE = (
    ('users.csv', User),
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    ('review.csv', Review),
    ('comments.csv', Comment),
    ('genre_title.csv', GenreTitle),
)

MODELS_FIELDS = {
    'category': Category,
    'genre': Genre,
    'title': Title,
    'review': Review,
    'author': User,
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов!'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        print(f'Загрузка данных в БД ...')
        for item in CSV_BASE:
            file_path = f'static/data/{item[0]}'
            model = item[1]
            with open(file_path, 'rt', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                columns: list = []
                i: int = 0
                for row in reader:
                    if i == 0:
                        columns.extend(row)
                    elif i > 0:
                        row_to_base: dict = {}
                        for j in range(0, len(row)):
                            if columns[j] in MODELS_FIELDS.keys():
                                temp_model = MODELS_FIELDS[columns[j]]
                                row[j] = get_object_or_404(temp_model, pk=row[j])
                            row_to_base.update({columns[j]: row[j]})
                        try:
                            obj, created = model.objects.get_or_create(**row_to_base)
                            if not created:
                                print(f"{obj} уже существует!")
                        except Exception as err:
                            print(f"NB Ошибка в строке {row}: {err}")
                    i += 1
        print('Загрузка данных в БД завершена!!!')
