# Generated by Django 4.0.4 on 2022-05-10 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_atividade_alunosatividade'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='turma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.turma'),
            preserve_default=False,
        ),
    ]
