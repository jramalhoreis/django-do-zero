# Modulos Nativos Python
import csv
from datetime import datetime


# Modulos do Django
from django.core.management.base import BaseCommand
from django.conf import settings


# Modulo de Terceiros


# Modulos do App
from polls.models import Question


class Command(BaseCommand):
    help="Data Command"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Arquivo CSV")

    def handle(self, *args, **kwargs):
        csv_file = open(f'{settings.BASE_DIR}/{kwargs.get("csv_file")}')
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            print(f'\nrow {row}')
            print(f'question_text: { row.get("question_text")}')
            print(f'pub_date.....: { row.get("pub_date")}')
            pub_date = datetime.fromisoformat(row.get('pub_date'))
            #pub_date = datetime.fromisoformat(row['pub_date'])
            question = Question (
                question_text = row.get('question_text'),
                pub_date = pub_date
            )

            question.save()
        

