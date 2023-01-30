# Generated by Django 4.1.5 on 2023-01-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainerName', models.CharField(max_length=255)),
                ('trainerLink', models.URLField(max_length=255)),
                ('doj', models.DateField()),
                ('trainer_type', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
            ],
        ),
    ]
