# Generated by Django 4.1.4 on 2023-01-02 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_company_location'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(blank=True, max_length=20, null=True)),
                ('deskCount', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('status', models.IntegerField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.company')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.employee')),
            ],
        ),
    ]
