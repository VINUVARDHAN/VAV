# Generated by Django 5.0.4 on 2024-04-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VAV', '0003_alter_userdetails_email_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile_image',
            field=models.ImageField(default='profile_images/default.png', upload_to='profile_images/'),
        ),
    ]
