# Generated by Django 3.2 on 2021-04-09 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_rename_student_pointrecord_studentid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointrecord',
            name='mothod',
        ),
    ]
