# Generated by Django 4.0.4 on 2022-05-10 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_aluno_confirmado'),
    ]

    operations = [
        migrations.AddField(
            model_name='alunosturma',
            name='pontuacao',
            field=models.FloatField(default=0, verbose_name='Pontuação'),
        ),
    ]
