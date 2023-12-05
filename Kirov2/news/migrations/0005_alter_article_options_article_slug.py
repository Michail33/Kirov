# Generated by Django 4.2.7 on 2023-12-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_tag_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['title', 'date'], 'verbose_name': 'Новост', 'verbose_name_plural': 'Новостииии'},
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=0),
            preserve_default=False,
        ),
    ]
