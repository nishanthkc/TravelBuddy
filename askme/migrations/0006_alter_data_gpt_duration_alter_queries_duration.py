# Generated by Django 4.0.7 on 2023-03-07 12:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0005_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='gpt_duration',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Duration must be greater than 1 character')]),
        ),
        migrations.AlterField(
            model_name='queries',
            name='duration',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Duration must be greater than 1 character')]),
        ),
    ]
