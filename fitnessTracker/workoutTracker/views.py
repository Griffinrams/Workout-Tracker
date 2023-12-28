import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout, Exercise, PlannedDay, RecordedDay, Location
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from django.core import serializers


# Create your views here.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id)
        workout_data = serializers.serialize('json', [workout])
        
        return JsonResponse({'workout': workout_data})
    except Workout.DoesNotExist:
        return JsonResponse({'error': 'Workout not found'}, status=404)

def check_recorded_day(request, date_str):
    try:
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if a RecordedDay object exists for the given date
        recorded_day = RecordedDay.objects.filter(date=date).first()
        
        
        if recorded_day is not None:
            # The object was found or created, and you can access its attributes
            exists = True
            # Access other attributes or perform operations on recorded_day
            workouts = recorded_day.workouts.all()
        else:
            # The object was not found or could not be created
            exists = False
            workouts = []  # Set workouts to an empty list or handle it as needed

                
        response_data = {
            'exists': exists,
            'workouts': [workout.title for workout in workouts]
        }
        return JsonResponse(response_data)
    
    except ValueError:
        # Handle the case where the date_str is not in the correct format
        return JsonResponse({'error': 'Invalid date format'})


def get_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id)
        workout_data = serializers.serialize('json', [workout])
        
        return JsonResponse({'workout': workout_data})
    except Workout.DoesNotExist:
        return JsonResponse({'error': 'Workout not found'}, status=404)

def home(request):
    today = date.today()
    num_days = 50  # Number of days to display
    end_date = today + timedelta(days=num_days)  # Calculate end date

    # Retrieve all planned days within the specified date range
    planned_days = PlannedDay.objects.filter(date__range=(today, end_date)).order_by('date')
    
    planned_workouts = {}
    
    for planned_day in planned_days:
        # Retrieve the workouts associated with the planned day
        workouts = planned_day.workouts.all()

        # Create a list to hold the workout details for the current day
        workout_details = []

        for workout in workouts:
            workout_details.append({
                'title': workout.title,
                'type': workout.workout_type,
            })

        # Add the workout details to the planned workouts dictionary using the date as the key
        planned_workouts[str(planned_day.date)] = workout_details

    context = {
        'planned_workouts': planned_workouts,
        'today': today,
        'num_days': num_days,
    }
    return render(request, 'workoutTracker/home.html', context)
    
def plan_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workoutId')
        planned_date_str = request.POST.get('date')
        #print(planned_date_str)
        date = datetime.strptime(planned_date_str, '%Y-%m-%d').date()
        day = PlannedDay.objects.create(date=date)
        #print(workout_id)
        workout = Workout.objects.get(id=workout_id)
        day.workouts.add(workout)
        

        # Return a JSON response indicating success or failure
        return JsonResponse({'message': 'Workout successfully planned'})
    else:
        # Return a JSON response with an error message
        return JsonResponse({'error': 'Invalid request method'}, status=400)
 
def successfulPlan(request):
    return render(request, "workoutTracker/successfulPlan.html")

def choose_date(request):
    if request.method == 'POST':
        Print("done")
    return render(request, 'workoutTracker/chooseDate.html')
    

    
def delete_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workoutId')
        # Perform the actual deletion logic
        Workout.objects.filter(id=workout_id).delete()

        # Return a JSON response indicating success or failure
        return JsonResponse({'message': 'Workout deleted successfully'})
    else:
        # Return a JSON response with an error message
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def edit_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)

    if request.method == 'POST':
        # Get the updated workout details from the form
        title = request.POST.get('title')
        workout_type = request.POST.get('workout_type')
        
        # Update the workout object with the new values
        workout.title = title
        workout.workout_type = workout_type
        workout.save()
        
        # Handle updating exercises if needed
        exercise_names = request.POST.getlist('exercise_name')
        workout.exercises.clear()  # Clear existing exercises associated with the workout
        
        for exercise_name in exercise_names:
            exercise = Exercise.objects.create(name=exercise_name)
            workout.exercises.add(exercise)
        
        return redirect('workout_detail', workout_id=workout.id)

    return render(request, 'workoutTracker/edit_workout.html', {'workout': workout})


def view_workouts(request):
    workouts = Workout.objects.all()
    context = {'workouts': workouts}
    return render(request, 'workoutTracker/view_workouts.html', context)
    
def user_workout(request):
    workouts = Workout.objects.all()
    return render(request, 'workoutTracker/user_workouts.html', {'workouts': workouts})
    
def planAhead(request):
    workouts = Workout.objects.all()
    context = {'workouts': workouts}
    return render(request, 'workoutTracker/planAhead.html', context)
    

def create_workout(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        workout_type = request.POST.get('workout_type')

        # Create the workout for the current user
        workout = Workout.objects.create(
            title=title,
            workout_type=workout_type
        )
        
        exercise_names = request.POST.getlist('exercise_name')
        for exercise_name in exercise_names:
            exercise = Exercise.objects.create(name=exercise_name)
            workout.exercises.add(exercise)
        return redirect('workout_detail', workout_id=workout.id)
    return render(request, 'workoutTracker/create_workout.html')
    
def create_workout_to_record(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        workout_type = request.POST.get('workout_type')

        # Create the workout for the current user
        workout = Workout.objects.create(
            title=title,
            workout_type=workout_type
        )
        
        exercise_names = request.POST.getlist('exercise_name')
        for exercise_name in exercise_names:
            exercise = Exercise.objects.create(name=exercise_name)
            workout.exercises.add(exercise)
        
        return redirect('user_workout')
    return render(request, 'workoutTracker/create_workout_to_record.html')



def add_location(request):
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        if Location.objects.filter(name=location_name).exists():
            return JsonResponse({'success': False, 'message': 'A location with this name already exists'})
        else:
            try:
                new_location = Location.objects.create(name=location_name)
                new_location.save()
                return JsonResponse({'success': True, 'location_name': new_location.name, 'message': 'Location created successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': 'An error occurred while creating the location.'})
    
    locations = Location.objects.all()
    context = {'locations': locations}
    
    return render(request, 'workoutTracker/AddLocation.html', context)
    
def delete_location(request, location_id):
    # Delete the location with the given ID
    location_to_delete = Location.objects.get(pk=location_id)
    location_to_delete.delete()
    return redirect('add_location')
    
def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)  
    return render(request, 'workoutTracker/workout_details.html', {'workout': workout})

def submit_data(request):
    locations = Location.objects.all()
    context = {'locations': locations}
    if request.method == 'POST':
   
        # Get user input from request.POST
        # Authenticate using service account credentials
        creds = None
        file_path_creds = 'C:/Users/griff/Documents/Python Project/fitnessTracker/workoutTracker/credentials.json'
        file_path_token = 'C:/Users/griff/Documents/Python Project/fitnessTracker/workoutTracker/token.json'
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(file_path_token):
            creds = Credentials.from_authorized_user_file(file_path_token, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    file_path_creds, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(file_path_token, 'w') as token:
                token.write(creds.to_json())
        service = build('sheets', 'v4', credentials=creds)

        # ID of the Google Sheets spreadsheet
        spreadsheet_id = '1vWu-n4c2leTtCzS41XTj6su-x4hKPIWx23SdjpxGzpY'

        # Range where the data should be written (e.g., Sheet1!A1)
        
        sheet_name = 'Sheet1'
        range_name = f'{sheet_name}!A:F'
        
        # Prepare the data to be written
        dateString = request.POST.get('hiddenDate')
        workout = request.POST.get('customWorkout')
        type = request.POST.get('Type')
        location = request.POST.get('Location')
        quality = request.POST.get('Quality')
        description = request.POST.get('Description')
        workout_id = request.POST.get('selectedWorkoutId')
        values = [[dateString, workout, type, location, quality, description]]
        
        
        #creaing a RecordedDay object
        workout = get_object_or_404(Workout, id=workout_id)
        date = datetime.strptime(dateString, '%Y-%m-%d').date()
        recorded_day = RecordedDay.objects.filter(date=date).first()
        if not recorded_day:
            recorded_day = RecordedDay.objects.create(date=date)
        recorded_day.workouts.add(workout)
           
        if recorded_day:
            print("RecordedDay object was created successfully.")
            print("Date:", recorded_day.date)
            print("Workouts:", recorded_day.workouts.all())
        else:
            print("RecordedDay object does not exist or was not created properly.")

        
        # Get the existing data in the spreadsheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        existing_values = result.get('values', [])
        
            # Find the first blank row from the top
        row_index = len(existing_values) + 1

        # Range to update (single row)
        update_range = f'{sheet_name}!A{row_index}:F{row_index}'

        # Write the data to the spreadsheet
        request_body = {
            'values': values
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=update_range,
            valueInputOption='USER_ENTERED',
            body=request_body
        ).execute()

        return render(request, 'workoutTracker/success.html')
    return render(request, 'workoutTracker/submit_form.html', context)

