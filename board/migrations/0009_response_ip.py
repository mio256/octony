# Generated by Django 3.2.7 on 2021-10-20 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_remove_response_ng_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='ip',
            field=models.CharField(default='null', max_length=32),
            preserve_default=False,
        ),
    ]
