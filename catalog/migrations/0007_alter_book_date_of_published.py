# Generated by Django 4.0.4 on 2022-04-16 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_book_date_of_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date_of_published',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
