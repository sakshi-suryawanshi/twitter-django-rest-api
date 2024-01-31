# Generated by Django 5.0.1 on 2024-01-31 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_user_following_userfollowers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers_list',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='base.user'),
        ),
        migrations.DeleteModel(
            name='UserFollowers',
        ),
    ]
