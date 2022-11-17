from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    appid = "9167ed92474dcfa53c4bfd87a49662a9"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()

                if res['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Такого города не существует'
            else:
                err_msg = 'Этот город уже есть в списке'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город успешно добавлен'
            message_class = 'is-success'

    form = CityForm

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'feels_like': res["main"]["feels_like"],
            'humidity': res["main"]["humidity"],
            'icon': res["weather"][0]["icon"],
            'speed': res["wind"]["speed"],
            'weather': res["weather"][0]["main"],

        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/index.html', context)

def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()

    return redirect('home')

