# Generated by Django 4.0.7 on 2023-06-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search_history',
            name='test_text',
            field=models.CharField(default='none', max_length=30),
        ),
    ]
