# Generated by Django 4.0.10 on 2025-03-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('act1', '0003_alter_trabajador_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacion',
            name='tiempo_operacion',
            field=models.FloatField(blank=True, null=True, verbose_name='Tiempo de Operación (horas)'),
        ),
    ]
