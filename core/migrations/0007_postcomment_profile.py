# Generated by Django 5.1 on 2024-09-19 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post_profile'),
        ('user', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_comments', to='user.profile'),
            preserve_default=False,
        ),
    ]
