# Generated by Django 3.2.9 on 2021-11-28 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('assignee_id', models.IntegerField(max_length=200)),
                ('collaborator_ids', models.JSONField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('custom_fields', models.JSONField()),
                ('description', models.CharField(max_length=200)),
                ('due_at', models.DateTimeField()),
                ('external_id', models.CharField(max_length=200)),
                ('follower_ids', models.JSONField()),
                ('group_id', models.IntegerField(max_length=200)),
                ('has_incidents', models.BooleanField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('organization_id', models.IntegerField(max_length=200)),
                ('priority', models.CharField(max_length=200)),
                ('problem_id', models.IntegerField(max_length=200)),
                ('raw_subject', models.CharField(max_length=200)),
                ('recipient', models.EmailField(max_length=254)),
                ('requester_id', models.IntegerField(max_length=200)),
                ('satisfaction_rating', models.JSONField()),
                ('sharing_agreement_ids', models.JSONField()),
                ('status', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('submitter_id', models.IntegerField(max_length=200)),
                ('tags', models.JSONField()),
                ('type', models.CharField(max_length=200)),
                ('updated_at', models.DateTimeField()),
                ('url', models.URLField()),
                ('via', models.JSONField()),
            ],
        ),
    ]
