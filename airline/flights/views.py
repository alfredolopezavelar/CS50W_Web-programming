from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, 'flights/index.html', {
        'flights': Flight.objects.all()
    })


def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, 'flights/flight.html', {
        'flight':flight,
        'passengers' : flight.passengers.all(),
        #because we are adding a <form> to add passengers,
        #we need to add a list of the passengers that are not in the flight
        'non_passengers': Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == 'POST':
        flight = Flight.objects.get(pk=flight_id)
        #The data of which passenger you need to book 
        #will be in a form where the input name will be passenger
        #(request.POST['passenger'])

        #To get the passenger we add this code 
        passenger = Passenger.objects.get(pk=int(request.POST['passenger']))

        #After getting the flight and the passenger, we add the passenger to the flight 
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))
        #you give an args formatted as a tuple because the url nees the flight id to render the flight information