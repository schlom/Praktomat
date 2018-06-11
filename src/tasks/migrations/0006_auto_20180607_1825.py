# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htmlinjector',
            name='inject_in_solution_view',
            field=models.BooleanField(default=False, help_text='Indicates whether HTML code shall be injected in public solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='submission_date',
            field=models.DateTimeField(help_text='The time up until the user has time to complete the task. This time will be extended by one hour for those who just missed the deadline.'),
        ),
    ]