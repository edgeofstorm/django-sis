# Generated by Django 3.0.6 on 2020-06-04 10:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_auto_20200604_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='sheet',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', '.pdf', '.txt', 'txt'])]),
        ),
    ]
