# Generated by Django 3.2 on 2021-04-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0020_alter_booklist_share_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareimg',
            name='img',
            field=models.ImageField(blank=True, upload_to='share_img', verbose_name='圖片'),
        ),
    ]
