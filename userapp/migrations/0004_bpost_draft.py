# Generated by Django 3.2.8 on 2022-02-02 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_bpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpost',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]