# Generated by Django 4.2.13 on 2024-06-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='imagem',
            field=models.FileField(blank=True, default=None, null=True, upload_to='images/user'),
        ),
    ]