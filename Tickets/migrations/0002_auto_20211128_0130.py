# Generated by Django 3.2.9 on 2021-11-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='collaborator_ids',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='custom_fields',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='due_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='follower_ids',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sharing_agreement_ids',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='tags',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='via',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
