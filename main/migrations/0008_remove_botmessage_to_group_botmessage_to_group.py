# Generated by Django 5.1.7 on 2025-04-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_groupmod_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botmessage',
            name='to_group',
        ),
        migrations.AddField(
            model_name='botmessage',
            name='to_group',
            field=models.ManyToManyField(related_name='guruhlar', to='main.groupmod', verbose_name='guruh/kanal'),
        ),
    ]
