# Generated by Django 3.0.6 on 2020-06-06 04:19

import datetime
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0015_auto_20200606_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 7, 19, 32, 929798)),
        ),
        migrations.AlterField(
            model_name='examstudentanswer',
            name='answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]
