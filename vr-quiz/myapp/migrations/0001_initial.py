# Generated by Django 4.2.11 on 2025-07-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('answers', models.TextField(blank=True, null=True)),
                ('player_answers', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField()),
                ('correctly_answered', models.TextField(blank=True, null=True)),
                ('passed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
