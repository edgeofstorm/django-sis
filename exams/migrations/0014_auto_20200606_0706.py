# Generated by Django 3.0.6 on 2020-06-06 04:06

import datetime
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0013_auto_20200606_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={'F': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'], 'M': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'], 'S': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'], 'T': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D']}, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 7, 6, 30, 12225)),
        ),
    ]
