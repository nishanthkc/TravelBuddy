# Generated by Django 4.0.7 on 2023-10-20 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askme', '0002_personaliseddata_user_alter_queries_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalisedFoodData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_food_id', models.CharField(editable=False, max_length=30, unique=True)),
                ('p_food_place', models.CharField(max_length=30)),
                ('p_food_result', models.TextField(max_length=100000)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
