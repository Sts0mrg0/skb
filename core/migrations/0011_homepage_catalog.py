# Generated by Django 2.2.5 on 2019-10-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photolog', '0003_auto_20191002_1345'),
        ('core', '0010_auto_20190328_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='catalog',
            field=models.ManyToManyField(blank=True, to='photolog.Catalog', verbose_name='Случайные фото из каталогов'),
        ),
    ]