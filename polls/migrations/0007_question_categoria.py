# Generated by Django 4.2.13 on 2024-07-03 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_question_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='categoria',
            field=models.CharField(choices=[('geral', 'Geral'), ('preferencias', 'Preferencias'), ('politica', 'Politica')], default=None, max_length=15, null=True, verbose_name='Categoria'),
        ),
    ]
