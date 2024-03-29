# Generated by Django 2.2.9 on 2020-10-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, related_name='groups', to='posts.Group'),
        ),
    ]
