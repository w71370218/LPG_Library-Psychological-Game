# Generated by Django 3.2 on 2021-04-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_auto_20210410_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
