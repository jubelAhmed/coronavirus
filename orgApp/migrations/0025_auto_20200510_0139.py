# Generated by Django 3.0.4 on 2020-05-09 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgApp', '0024_auto_20200510_0136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orgproject',
            options={'get_latest_by': '-created_date'},
        ),
    ]
