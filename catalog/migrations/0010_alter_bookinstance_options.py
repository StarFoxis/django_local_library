# Generated by Django 4.0.4 on 2022-04-17 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('syka', 'Rabotai tvar'),)},
        ),
    ]
