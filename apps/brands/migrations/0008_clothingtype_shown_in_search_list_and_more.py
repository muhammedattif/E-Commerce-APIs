# Generated by Django 4.1.7 on 2023-03-17 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0007_homepagesection'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothingtype',
            name='shown_in_search_list',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='homepagesection',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepagesection',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]