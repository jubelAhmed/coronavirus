# Generated by Django 3.0.4 on 2020-05-09 00:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgApp', '0022_auto_20200509_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='about',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='orgproject',
            name='details',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]