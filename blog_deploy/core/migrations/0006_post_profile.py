# Generated by Django 5.1 on 2024-09-17 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_feedback_alter_post_options'),
        ('user', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_posts', to='user.profile'),
            preserve_default=False,
        ),
    ]