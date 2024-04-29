# Generated by Django 5.0.1 on 2024-02-29 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0006_gas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('Gid', models.BigAutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('subsidy', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='Gas',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='num_of_orders',
        ),
    ]
