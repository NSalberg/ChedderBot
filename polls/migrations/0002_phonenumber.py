# Generated by Django 4.2.7 on 2023-11-14 00:08

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
    ]