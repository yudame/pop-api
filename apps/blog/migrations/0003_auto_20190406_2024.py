# Generated by Django 2.1.2 on 2019-04-06 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0002_auto_20190406_2024'),
        ('blog', '0002_auto_20190406_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author_anonymous',
        ),
        migrations.RemoveField(
            model_name='article',
            name='authored_at',
        ),
        migrations.AddField(
            model_name='blog',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='unpublished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='trello_label',
            field=models.OneToOneField(default="c26bded4-4042-47aa-bbcb-35bb8b27166c", on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='trello.Label'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='unpublished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
