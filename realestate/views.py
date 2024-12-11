from django.shortcuts import render
from django.http import JsonResponse
from realestate.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import logging
from random import choice
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):

    houses = House.objects.all() 
    context = {'houses':houses}
    return render(request, 'index.html', context)

def house(request, id):
    house = House.objects.get(id=id)

    # зчитуємо поточну дату та час
    today = datetime.now().date()
    time_now = datetime.now()  

    # список для доступних записів
    appointmentsFree = []

    # проходимся по наступних 3 днях
    for day_offset in range(3):
        date = today + timedelta(days=day_offset)

        # Час з 9:00 до 16:00 з проміжком в годину
        for hour in range(9, 17):
            time_interval = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)

            # Пропускаємо часи які були вже
            if time_interval > time_now:

                # Перевіряємо чи вже є запис
                apointments =  Appointment.objects.filter(
                    house=house, time=time_interval
                ).exists()

                # Перевірка чи є вільні ріелтори
                realtor_busy =  Appointment.objects.filter(
                    time=time_interval
                ).exclude(realtor__isnull=True).exists()

                if not apointments and not realtor_busy:
                    appointmentsFree.append({'datetime': time_interval})

    context = {
        'house': house,
        'freeAppointments': appointmentsFree
    }
    return render( request, 'house.html', context)




@csrf_exempt
def appointment(request):
    data = json.loads(request.body)
    phone = data.get('phone')
    name = data.get('name')
    houseId = data.get('houseId')
    data_and_time_str = data.get('datetime')
    data_and_time = datetime.strptime(data_and_time_str, '%Y-%m-%d %H:%M')

    # Знаходимо вільних ріелторів
    busyRealtors = Realtor.objects.filter(appointments__time=data_and_time)
    freeRealtors = Realtor.objects.exclude(id__in=busyRealtors.values_list('id', flat=True))

    if not freeRealtors.exists():
        return JsonResponse({'error': 'Немає вільних ріелторів. Спробуйте інший час'}, status=400)

    # Додаємо клієнта до бази
    client, created = Client.objects.get_or_create(phone_number = phone, name = name)
    
    realtor = choice(freeRealtors)

    appointment = Appointment.objects.create(
        client=client,
        realtor=realtor,
        house_id=houseId, 
        time=data_and_time
    )

    return JsonResponse({'message': 'Запис створено успішно.'}, status=200)


def realtor(request):
    realtors = Realtor.objects.all() 
    context = {'realtors':realtors}
    return render(request, 'realtors.html', context)


def get_realtor_tasks(request, realtor_id):
    try:
        selected_realtor = Realtor.objects.get(id=realtor_id)
        
        # Отримуємо час зараз
        time_now = timezone.now()
        
        # Фукаєм всі майбутні завдання 
        tasks =  selected_realtor.appointments.filter(time__gte=  time_now).order_by( 'time')

        tasks_data = [
            {
                'time': task.time.strftime('%Y-%m-%d %H:%M'),
                'house': {
                    'id': task.house.id,
                    'address': task.house.address,
                    'url': reverse('house', args=[task.house.id]) 
                },
                'client': {
                    'name': task.client.name,
                    'phone': task.client.phone_number
                }
            }
            for task in tasks
        ]
        
        return JsonResponse({'tasks': tasks_data})
    except Realtor.DoesNotExist:
        return JsonResponse( {'error': 'Realtor not found'}, status=404)

