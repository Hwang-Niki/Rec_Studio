from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from studio.models import Project
from .models import User
from django.db import IntegrityError
from .forms import ArtistForm, ProducerForm, ClientForm, ManagerForm
import logging
import json


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'studio/home.html')

def artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArtistForm()

    return render(request, 'studio/artist_form.html', {'form': form})


def producer(request):
    if request.method == 'POST':
        form = ProducerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProducerForm()
    return render(request, 'studio/producer_form.html', {'form': form})

def client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientForm()
    return render(request, 'studio/client_form.html', {'form': form})

def notification(request):
    return render(request, 'studio/notifications.html')

def notification_client(request):
    return render(request, 'studio/notifications_client.html')

def project(request):
    projects = Project.objects.all()  # Здесь может быть ваша логика фильтрации
    return render(request, 'studio/project.html', {'projects': projects})

def create_project(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project = Project.objects.create(
            name=data['name'],
            album_image=data['album_image'],  # Обработка загрузки файлов может потребовать дополнительных шагов
            end_date=data['end_date'],
            current_status=data['current_status'],
            performer=data['performer']
        )
        return JsonResponse({'id': project.id, 'message': 'Project created successfully!'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST 
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({'message': 'Project deleted successfully!'}, status=200)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found!'}, status=404)

@csrf_protect
def register(request):
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'role': request.POST.get('role'),
        }

        try:
            user = User(**user_data)
            user.set_password(user_data['password'])
            user.save()
            logging.info(f"Пользователь {user.username} был зарегистрирован успешно.")
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
        except ValueError as e:
            logging.error(f"Ошибка валидации: {e}")
            messages.error(request, f"Ошибка валидации: {e}")
            return render(request, 'register.html', {'user_data': user_data})
        except IntegrityError as e:
            logging.warning(f"Пользователь с именем {user_data['username']} уже существует.")
            messages.error(request, "Пользователь с таким именем уже существует.")
            return render(request, 'register.html', {'user_data': user_data})
        except Exception as e:
            logging.critical(f"Неизвестная ошибка: {e}")
            messages.error(request, f"Неизвестная ошибка: {e}")
            return render(request, 'studio/register.html', {'user_data': user_data})

    else:
        return render(request, 'studio/register.html')
    

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('Пользователь успешно вошел. Перенаправление на главную страницу.')

            # Получаем роль пользователя
            role = getattr(user, 'role', None)  # Предполагается, что у пользователя есть поле role

            # Перенаправление в зависимости от роли
            if role == 'artist':
                return redirect('artist') 
            elif role == 'producer':
                return redirect('producer')
            elif role == 'soundman':
                return redirect('soundman')  
            else:
                return redirect('client')  # На главную страницу для обычных пользователей
        else:
            logger.warning('Не удалось аутентифицировать пользователя.')
            error_message = "Не удалось аутентифицировать. Проверьте username и пароль."
            return render(request, 'studio/login.html', {'error_message': error_message})

    return render(request, 'studio/login.html')

def my_view(request):
    if request.user.is_authenticated:
        logger.info(f'Пользователь {request.user.username} с ролью {request.user.role}')
        role = request.user.role  # Это должно быть поле с ролью
        if role == 'artist':
            return redirect('artist_form')
        elif role == 'producer':
            return redirect('producer_form')
        else:
            return redirect('client_form')
    return redirect('home')  # Для неавторизованных пользователей






