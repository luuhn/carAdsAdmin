# Generated by Django 2.2.7 on 2019-11-27 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='num_cars',
            field=models.DecimalField(decimal_places=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='car',
            name='bank_account',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='car',
            name='bank_branch',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_color',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_seat',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='driver_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='car',
            name='status',
            field=models.BooleanField(blank=True),
        ),
        migrations.CreateModel(
            name='CarKpi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalDistance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateField()),
                ('province', models.CharField(max_length=50)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Car')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignKpi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalDistance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('province', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignHourly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalDistance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('hour', models.IntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
            ],
        ),
    ]
