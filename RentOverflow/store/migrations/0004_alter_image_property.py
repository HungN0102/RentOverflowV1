# Generated by Django 4.1.2 on 2023-07-16 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_property_imageid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.property', to_field='imageId'),
        ),
    ]
