# Generated by Django 2.2.7 on 2019-11-17 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping_recetas_app', '0002_auto_20191117_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recetas', to='scraping_recetas_app.Categoria'),
        ),
    ]