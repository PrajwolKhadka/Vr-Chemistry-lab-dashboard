# Generated by Django 4.2.11 on 2025-07-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_surveyresponse_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='surveyresponse',
            index=models.Index(fields=['modified_at'], name='myapp_surve_modifie_9e6cef_idx'),
        ),
    ]
