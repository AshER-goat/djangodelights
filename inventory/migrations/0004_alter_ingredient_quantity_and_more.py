# Generated by Django 5.0.3 on 2024-04-06 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_ingredient_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
