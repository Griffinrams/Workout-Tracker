from django.db import models

class Workout(models.Model):
    title = models.CharField(max_length=100)
    workout_type = models.CharField(max_length=100)
    exercises = models.ManyToManyField('Exercise', related_name='workouts')
   
    def __str__(self):
        return self.title

class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PlannedDay(models.Model):
    date = models.DateField()
    workouts = models.ManyToManyField('Workout', related_name='planned_days')
    
    def __str__(self):
        return str(self.date)
        
class RecordedDay(models.Model):
    date = models.DateField()
    workouts = models.ManyToManyField('Workout', related_name='recorded_days')
  
    def __str__(self):
        return str(self.date)
        
