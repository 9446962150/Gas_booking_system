# Generated by Django 5.0.1 on 2024-02-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0004_userprofile_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='num_of_orders',
            field=models.IntegerField(default=0),
        ),
    ]
