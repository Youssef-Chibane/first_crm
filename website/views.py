from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm  # Importing forms defined in forms.py
from .models import Record  # Importing the Record model from models.py


def home(request):
    records = Record.objects.all()  # Fetching all records from the Record model

    # Handling POST request for user login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticating user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in. Please try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)  # Logging out the user
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Creating SignUpForm instance with POST data
        if form.is_valid():
            form.save()  # Saving the form data to create a new user
            # Authenticating and logging in the new user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()  # Creating an empty SignUpForm instance for GET request
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)  # Fetching the specific record by its id
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be logged in to see this page.")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)  # Fetching the record to be deleted by its id
        delete_it.delete()  # Deleting the record
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)  # Creating AddRecordForm instance with POST data or None

    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()  # Saving the form data to add a new record
                messages.success(request, "Record added.")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)  # Fetching the record to be updated by its id
        form = AddRecordForm(request.POST or None, instance=current_record)  # Creating form instance with POST data or None
        
        if form.is_valid():
            form.save()  # Saving the updated form data
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
