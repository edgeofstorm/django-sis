# Generated by Django 3.0.6 on 2020-06-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]
