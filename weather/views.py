from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    # Fetch all cities from the database
    cities = City.objects.all()

    # Define the base URL for OpenWeatherMap API
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ac54df7369427aca98b7f2da1d1888b8"

    if request.method == 'POST':
        form = CityForm(request.POST)  # Bind the form with POST data
        if form.is_valid():  # Validate form data
            form.save()  # Save valid data to the database
            return redirect('index')  # Redirect to avoid resubmission on refresh
        else:
            form = CityForm()



    weather_data = []

    for city in cities:
        try:
            # Fetch weather data for the city
            response = requests.get(url.format(city.name))
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            city_weather = response.json()

            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }

            weather_data.append(weather)
        except (requests.exceptions.RequestException, KeyError):
            # Handle API request errors or missing keys gracefully
            continue

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)