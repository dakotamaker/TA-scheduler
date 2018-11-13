# Generated by Django 2.1.3 on 2018-11-13 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('act_email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('act_fname', models.CharField(max_length=50)),
                ('act_lname', models.CharField(max_length=50)),
                ('act_phone', models.CharField(max_length=15)),
                ('act_password', models.CharField(max_length=50)),
                ('act_address', models.CharField(max_length=255)),
                ('role_id', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=50)),
                ('instructor_email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instructor_email', to='app.Account')),
                ('ta_emails', models.ManyToManyField(related_name='ta_email', to='app.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('lab_id', models.IntegerField(primary_key=True, serialize=False)),
                ('lab_name', models.CharField(max_length=50)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('ta_email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Account')),
            ],
        ),
    ]
