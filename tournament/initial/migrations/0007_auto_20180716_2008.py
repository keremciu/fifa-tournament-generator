# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-16 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0006_auto_20170908_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='clubs',
            field=models.ManyToManyField(related_name='clubList', to='initial.Club'),
        ),
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.FileField(default=b'pic_folder/None/no-img.jpg', upload_to=b'pic_folder/'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='away_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='home_score',
            field=models.IntegerField(default=0),
        ),
    ]
