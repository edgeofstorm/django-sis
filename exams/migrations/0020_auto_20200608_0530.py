# Generated by Django 3.0.6 on 2020-06-08 02:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200608_0409'),
        ('exams', '0019_auto_20200608_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 8, 5, 30, 25, 344441)),
        ),
        migrations.AlterField(
            model_name='examsolution',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributed_solutions', to='users.Teacher'),
        ),
    ]
