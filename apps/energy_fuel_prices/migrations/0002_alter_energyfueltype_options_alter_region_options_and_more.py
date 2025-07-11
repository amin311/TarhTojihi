# Generated by Django 5.1.3 on 2024-12-22 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_fuel_prices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='energyfueltype',
            options={'verbose_name': 'نوع سوخت', 'verbose_name_plural': 'انواع سوخت'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'منطقه', 'verbose_name_plural': 'مناطق'},
        ),
        migrations.AlterField(
            model_name='energyfueltype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='energyfueltype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='region',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
    ]
