# Generated by Django 4.0 on 2022-04-03 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('routing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailed_address', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routing.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('contact_number', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('tracking_id', models.IntegerField(max_length=64)),
                ('current_tracking_status', models.CharField(max_length=64)),
                ('parcel_on_return', models.BooleanField(default=False)),
                ('destination_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_address', to='parcel_management.address')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='parcel_management.customer')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='parcel_management.customer')),
                ('source_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_address', to='parcel_management.address')),
            ],
        ),
    ]