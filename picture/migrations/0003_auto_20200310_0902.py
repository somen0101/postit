# Generated by Django 2.2.5 on 2020-03-10 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='user_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
