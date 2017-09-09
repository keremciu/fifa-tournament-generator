# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0005_auto_20170908_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
                ('is_played', models.BooleanField(default=False)),
                ('is_playoff_game', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='score',
            old_name='drawn',
            new_name='draw',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='season',
            new_name='season_id',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='team',
            new_name='team_id',
        ),
        migrations.AddField(
            model_name='season',
            name='prize',
            field=models.CharField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='club',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='initial.Team'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='away_team_club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awayclub', to='initial.Club'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='away_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayteam', to='initial.Team'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='home_team_club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='homeclub', to='initial.Club'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='home_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometeam', to='initial.Team'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='season_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='initial.Season'),
        ),
    ]