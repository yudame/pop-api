# Generated by Django 3.0.7 on 2020-06-25 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20200622_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalshop',
            name='unstructured_text_address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='shop',
            name='unstructured_text_address',
            field=models.TextField(blank=True, default=''),
        ),
    ]