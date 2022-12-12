# Generated by Django 4.1 on 2022-11-02 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlespage',
            name='title',
            field=models.CharField(error_messages={'unique': 'Article with this Title already exists.'}, help_text='Required. Must be unique. Letters and digit only with fewer than 150 word.', max_length=255, primary_key=True, serialize=False),
        ),
    ]
