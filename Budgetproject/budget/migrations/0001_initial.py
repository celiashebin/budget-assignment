# Generated by Django 3.0 on 2020-04-18 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
                ('expenses', models.IntegerField()),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
