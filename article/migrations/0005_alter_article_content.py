# Generated by Django 4.1.5 on 2023-04-08 04:04

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0004_alter_article_author_alter_article_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="content",
            field=ckeditor.fields.RichTextField(verbose_name="Article Content"),
        ),
    ]