# Generated by Django 5.1.4 on 2024-12-09 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0004_appointment_client_house_image_realtor_delete_houses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
