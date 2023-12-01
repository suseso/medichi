# Generated by Django 4.2.5 on 2023-11-17 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=30, verbose_name='apellido')),
                ('email', models.EmailField(max_length=150, verbose_name='email')),
                ('dni', models.PositiveIntegerField(unique=True, verbose_name='dni')),
                ('numeroAfiliado', models.CharField(max_length=100, verbose_name='numeroAfiliado')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Especialidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(max_length=150, unique=True, verbose_name='especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.IntegerField(choices=[(1, 'Plan 300'), (2, 'Plan 400'), (3, 'Plan Platinum')])),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=30, verbose_name='apellido')),
                ('email', models.EmailField(max_length=150, verbose_name='email')),
                ('dni', models.PositiveIntegerField(unique=True, verbose_name='dni')),
                ('matricula', models.IntegerField(verbose_name='matricula')),
                ('cuit', models.IntegerField(verbose_name='cuit')),
                ('especialidades', models.ManyToManyField(related_name='profesionales', to='app_principal.especialidades')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EspecialidadesProfesionales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.ManyToManyField(related_name='especialidades', to='app_principal.especialidades')),
                ('profesionales', models.ManyToManyField(related_name='nombre_profesional', to='app_principal.profesional')),
            ],
        ),
        migrations.CreateModel(
            name='CrearTurno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('disponible', models.BooleanField(default=True)),
                ('afiliado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_principal.afiliado')),
                ('especialidades', models.ManyToManyField(to='app_principal.especialidades')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_principal.profesional')),
            ],
        ),
        migrations.AddField(
            model_name='afiliado',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_principal.plan'),
        ),
    ]