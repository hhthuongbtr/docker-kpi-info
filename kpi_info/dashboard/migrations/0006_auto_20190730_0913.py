# Generated by Django 2.2.3 on 2019-07-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_revenue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revenue',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]