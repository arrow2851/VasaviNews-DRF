# Generated by Django 2.1 on 2018-08-23 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0004_remove_post_author_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all',
            name='banned_list',
        ),
        migrations.RemoveField(
            model_name='all',
            name='moderators',
        ),
        migrations.RemoveField(
            model_name='all',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='all',
            name='subscribers',
        ),
        migrations.DeleteModel(
            name='All',
        ),
    ]
