# Generated by Django 2.2.7 on 2019-12-19 08:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0010_auto_20191208_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportimage',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.CreateModel(
            name='UserCampaig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
