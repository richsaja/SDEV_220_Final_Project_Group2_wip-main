# Generated by Django 3.2.1 on 2023-07-27 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('helpcenter', '0004_alter_ticket_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='submitted_date',
        ),
        migrations.AddField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
