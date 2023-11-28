# Generated by Django 4.2.7 on 2023-11-28 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('weight', models.FloatField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Not Informed', 'Notinformed')], default='Not Informed', max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='groups.group')),
            ],
        ),
    ]
