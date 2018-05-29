# Generated by Django 2.0.2 on 2018-05-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='collector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_user', models.CharField(max_length=700)),
                ('name', models.CharField(max_length=250)),
                ('family', models.CharField(max_length=250)),
                ('Email', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('telephone', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dr_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dr_name', models.CharField(max_length=250)),
                ('Dr_family', models.CharField(max_length=250)),
                ('Dr_telephone', models.CharField(max_length=50)),
                ('Dr_google_map_link', models.CharField(max_length=700)),
                ('Dr_Address', models.CharField(max_length=700)),
                ('Dr_photo_link', models.CharField(max_length=700)),
            ],
        ),
    ]
