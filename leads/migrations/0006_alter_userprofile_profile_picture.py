# Generated by Django 5.0.1 on 2024-01-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
