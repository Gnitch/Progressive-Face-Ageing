# Generated by Django 3.2.3 on 2021-12-17 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_missing_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='brother',
            new_name='sibling',
        ),
        migrations.RemoveField(
            model_name='family',
            name='sister',
        ),
    ]