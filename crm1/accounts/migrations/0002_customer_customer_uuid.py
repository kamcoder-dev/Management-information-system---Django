# Generated by Django 3.0.6 on 2020-06-10 22:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
