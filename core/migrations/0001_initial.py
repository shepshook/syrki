# Generated by Django 3.0.5 on 2020-04-30 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('publication_date', models.DateTimeField()),
                ('likes', models.ManyToManyField(related_name='liked_posts', to='core.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to='core.Profile')),
            ],
            options={
                'ordering': ['-publication_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('publication_date', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Profile')),
            ],
        ),
    ]
