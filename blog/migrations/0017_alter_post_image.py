# Generated by Django 4.2 on 2023-05-03 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='moon.png', null=True, upload_to='images/', verbose_name='Load Image'),
        ),
    ]
