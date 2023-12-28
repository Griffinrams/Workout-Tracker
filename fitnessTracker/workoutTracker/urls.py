from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit_data, name="submit_data"),
    path("createWorkout/", views.create_workout, name="create_workout"),
    path("submit/user_workout/create_workout/", views.create_workout_to_record, name="create_workout_"),
    path('workout_detail/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('view_workouts/', views.view_workouts, name='view_workouts'),
    path("", views.home, name="home"),
    path('edit_workout/<int:workout_id>', views.edit_workout, name='edit_workout'),
    path('delete_workout/', views.delete_workout, name='delete_workout'),
    path('planAhead/', views.planAhead, name = 'planAhead'),
    path('plan_workout/', views.plan_workout, name = 'plan_workout'),
    path('successfulPlan/', views.successfulPlan, name = 'successfulPlan'),
    path('choose_date/', views.choose_date, name = 'choose_date'),
    path('submit/user_workout/', views.user_workout, name = 'user_workout'),
    path('get_workout/<int:workout_id>/', views.get_workout, name='get_workout'),
    path('check_recorded_day/<str:date_str>/', views.check_recorded_day, name='check_recorded_day'),
    path('submit/add_location/', views.add_location, name = 'add_location'),
    path('submit/delete_location/<int:location_id>/', views.delete_location, name='delete_location'),

]