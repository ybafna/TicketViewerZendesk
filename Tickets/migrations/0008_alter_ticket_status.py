# Generated by Django 3.2.9 on 2021-11-28 23:21

from django.db import migrations, models
import io


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0007_auto_20211128_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=io.open, max_length=200),
            preserve_default=False,
        ),
    ]