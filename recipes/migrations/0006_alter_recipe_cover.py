# Generated by Django 4.2.3 on 2023-08-22 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/cover/%Y/%m/%d/'),
        ),
    ]