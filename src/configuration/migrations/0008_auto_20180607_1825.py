# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_settings_final_grades_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Setting', 'verbose_name_plural': 'Settings'},
        ),
        migrations.AlterField(
            model_name='settings',
            name='attestation_allow_run_checkers',
            field=models.BooleanField(default=False, help_text='If enabled, tutors can re-run all checkers for solutions they attest. Can be used to re-run checks that failed due to problems unrelated to the solution (e.g.: time-outs because of high server-load), but needs to be used with care, since it may change the results from what the student saw when he submitted his solution.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='invisible_attestor',
            field=models.BooleanField(default=False, help_text='If enabeld, users will not learn which tutor wrote attestations to his solutions. In particular, tutors will not be named in Attestation-Emails.'),
        ),
    ]