# Generated by Django 2.2.5 on 2019-10-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_images_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='size',
            field=models.SmallIntegerField(choices=[(180, '180'), (300, '300'), (600, '600'), (800, '800')], default='300'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='blog/cover', verbose_name='Обложка'),
        ),
    ]
