# Generated by Django 3.0.7 on 2020-07-20 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line_app', '0017_auto_20200720_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linechannelmembership',
            name='current_rich_menu',
        ),
    ]
