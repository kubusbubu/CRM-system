# Generated by Django 3.1.4 on 2023-12-10 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20231201_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]