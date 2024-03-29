# Generated by Django 4.0.5 on 2022-07-06 13:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_status_alter_bid_bid_amt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_bid', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 6, 13, 2, 45, 640562, tzinfo=utc), editable=False),
        ),
    ]
