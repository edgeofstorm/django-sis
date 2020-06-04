# Generated by Django 3.0.6 on 2020-06-04 09:27

from django.db import migrations, models
import exams.validators


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_auto_20200604_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='sheet',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[exams.validators.validate_file_extension]),
        ),
    ]
