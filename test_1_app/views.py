from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], birthday=request.POST['birthday'], password=hashed_pw)
            request.session['user_id'] = user.id
    return redirect('/success')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/success')
        messages.error(request, "Email or password is incorrect.")
        return redirect('/')

def welcome(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'trips': Trip.objects.all()
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def create_trip(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    return render(request, 'add_trip.html')

def add_trip(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    errors = Trip.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trip/create')
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        this_trip = Trip.objects.create(destination=request.POST['destination'], plan=request.POST['plan'], date_from=request.POST['date_from'], date_to=request.POST['date_to'], creator=user)
        this_trip.attendees.add(user)
        return redirect('/success')

def remove_trip(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            user = user[0]
        trip_to_remove = Trip.objects.filter(id=id)
        if len(trip_to_remove) > 0:
            trip_to_remove = trip_to_remove[0]
        user.trips_attending.remove(trip_to_remove)
        return redirect('/success')

def delete_trip(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            user = user[0]
        trip_to_delete = Trip.objects.filter(id=id)
        if len(trip_to_delete) > 0:
            trip_to_delete = trip_to_delete[0]
        if trip_to_delete in user.created_trips.all():
            trip_to_delete.delete()
            return redirect('/success')
        else:
            messages.error(request, "You must be trip creator to delete trip.")
            return redirect('/success')

def join_trip(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "POST":
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0:
            user = user[0]
        trip_to_join = Trip.objects.filter(id=id)
        if len(trip_to_join) > 0:
            trip_to_join = trip_to_join[0]
        user.trips_attending.add(trip_to_join)
        return redirect('/success')

def view_trip(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'trip': Trip.objects.get(id=id)
    }
    return render(request, 'view_trip.html', context)




# Create your views here.
