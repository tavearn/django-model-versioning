# Generated by Django 5.0.2 on 2024-03-03 16:28

import django.db.models.deletion
import lib.versioned_foreign_key
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tax', lib.versioned_foreign_key.VersionedForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='taxes.tax')),
            ],
        ),
    ]
