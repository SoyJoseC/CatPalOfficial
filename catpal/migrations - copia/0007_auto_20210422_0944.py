# Generated by Django 3.1.3 on 2021-04-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catpal', '0006_auto_20210422_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='year',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
