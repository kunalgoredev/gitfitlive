# Generated by Django 4.2 on 2023-11-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_core', '0005_alter_question_options_option_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='triggers_date_picker',
            field=models.BooleanField(default=False),
        ),
    ]