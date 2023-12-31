# Generated by Django 4.2.1 on 2023-05-30 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutTracker', '0006_remove_exercise_workout_workout_exercises'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='workout',
            name='planned_days',
            field=models.ManyToManyField(related_name='workouts', to='workoutTracker.plannedday'),
        ),
    ]
