# Generated by Django 5.1.1 on 2024-09-30 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_user_auctionlisting_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='image',
            new_name='image_url',
        ),
    ]
