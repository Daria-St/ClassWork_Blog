# Generated by Django 5.1 on 2024-09-24 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_subscription'),
        ('user', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dare', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to='core.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_like', to='user.profile')),
            ],
            options={
                'verbose_name': 'Лайк поста',
                'verbose_name_plural': 'Лайки постов',
            },
        ),
    ]