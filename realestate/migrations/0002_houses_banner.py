# Generated by Django 5.1.4 on 2024-12-08 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='houses',
            name='banner',
            field=models.ImageField(blank=True, default='logo.png', upload_to=''),
        ),
    ]