# Generated by Django 2.0.2 on 2018-05-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Super_users', '0014_auto_20180527_0816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hash_capcha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hash_value', models.CharField(max_length=1000)),
                ('Number', models.CharField(max_length=13)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='description',
        ),
        migrations.RemoveField(
            model_name='document',
            name='uploaded_at',
        ),
        migrations.AddField(
            model_name='document',
            name='path',
            field=models.CharField(default=1000, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=''),
        ),
    ]
