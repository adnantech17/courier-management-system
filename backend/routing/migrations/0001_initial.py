# Generated by Django 4.0 on 2022-04-01 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('estimated_processing_time', models.FloatField()),
                ('estimated_processing_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BranchEdge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_time', models.FloatField()),
                ('shipping_cost', models.FloatField()),
                ('from_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_branch', to='routing.branch')),
                ('to_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_branch', to='routing.branch')),
            ],
        ),
    ]
