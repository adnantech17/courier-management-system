# Generated by Django 4.0 on 2022-04-16 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel_management', '0004_parcel_current_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathhistory',
            name='status',
            field=models.CharField(default='Received at', max_length=20),
        ),
    ]