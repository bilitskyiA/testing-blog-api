# Generated by Django 2.2 on 2020-07-11 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Unlike'), (0, 'Null')], default=0),
        ),
    ]
