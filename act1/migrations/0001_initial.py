# Generated by Django 3.2 on 2025-03-11 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('tipo', models.IntegerField()),
                ('estado', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=45)),
                ('tipo', models.CharField(max_length=45)),
                ('estado_maquina', models.CharField(max_length=45)),
                ('cilindraje', models.CharField(max_length=45)),
                ('modelo', models.IntegerField()),
                ('serial', models.CharField(max_length=45)),
                ('disponibilidad', models.CharField(max_length=2)),
                ('kilometraje', models.IntegerField()),
                ('tipo_combustible', models.CharField(max_length=45)),
                ('complemento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='act1.complemento')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('apellido', models.CharField(max_length=45)),
                ('cedula', models.IntegerField()),
                ('telefono', models.BigIntegerField()),
                ('pin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField()),
                ('fecha_salida', models.DateTimeField()),
                ('area', models.CharField(max_length=100)),
                ('consumo', models.CharField(max_length=45)),
                ('observaciones', models.TextField()),
                ('tiempo_operacion', models.IntegerField()),
                ('tipo_operacion', models.CharField(max_length=45)),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='act1.maquina')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='act1.trabajador')),
            ],
        ),
    ]
