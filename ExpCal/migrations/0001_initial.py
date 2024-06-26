# Generated by Django 5.0.2 on 2024-02-25 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('VAV', '0003_alter_userdetails_email_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('categoryId', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VAV.userdetails')),
            ],
        ),
        migrations.CreateModel(
            name='ExpDetails',
            fields=[
                ('expId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('additional_info', models.TextField(default='---')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('categoryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ExpCal.categoryinfo')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VAV.userdetails')),
            ],
        ),
    ]
