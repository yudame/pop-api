# Generated by Django 2.1.2 on 2019-04-06 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='blog.Blog'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='blog',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='blog.Blog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='trello_card',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='trello.Card'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='parent_blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_blogs', to='blog.Blog'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='trello_board',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to='trello.Board'),
        ),
    ]
