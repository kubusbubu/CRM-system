# Generated by Django 5.0.1 on 2024-01-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0008_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='static/images/default.png', null=True, upload_to='media/profile_pics/'),
        ),
    ]