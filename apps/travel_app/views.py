from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from .models import *
from django.core.urlresolvers import reverse

def index(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    me = User.objects.get(id = request.session['user_id'])
    mytrips = Buddy.objects.filter(traveler = me)
    joined = []
    for each in mytrips:
        joined.append(each.trip)

    other_trips = Buddy.objects.all().exclude(traveler = me)
    not_joined = []
    for each in other_trips:
        not_joined.append(each.trip)

    to_display = []
    for each in not_joined:
        if each not in joined:
            to_display.append(each)
    
    print mytrips
    context = {
        'mytrips':mytrips,
        'other':to_display,
    }
    return render(request, "travel_app/index.html", context)

def logout(request):
    request.session.flush()
    return redirect('log_reg:index')

def add(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    return render(request, "travel_app/add.html")

def create_trip(request):
    if request.method == "POST":
        result = Trip.objects.create_trip(request.POST)
        if result[0] == False:
            context = {'errors':result[1]}
            return render(request, "travel_app/add.html", context)
        if result[0] == True:
            print Trip.objects.all()
            return redirect('travel_app:index')

def join(request, trip_id):
    print trip_id, "&&&^^&^*&^*^&*^%*^&^%*&^%^"
    trip = Trip.objects.get(id = trip_id)
    me = User.objects.get(id = request.session['user_id'])
    Buddy.objects.create_plan(me, trip)
    return redirect('travel_app:index')


def info(request, trip_id):
    me = User.objects.get(id = request.session['user_id'])
    the_trip = Trip.objects.get(id = trip_id)
    travelers = Buddy.objects.exclude(traveler = me).filter(trip = the_trip)
    others = []
    for each in travelers:
        others.append(each.traveler)
    context = {
        'trip':the_trip,
        'users':others,
    }
    return render(request, "travel_app/info.html", context)
# Create your views here.
