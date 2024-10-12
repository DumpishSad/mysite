import os

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('username', 'Неверное имя пользователя или пароль')
    return render(request, 'login.html', {'form': form})


def editor_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        image_name = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(image_name)
        return render(request, 'editor.html', {'image_url': image_url})

    return render(request, 'editor.html')


def download_image(request, filename):
    # Путь к файлу в MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Создаем HTTP-ответ с содержимым файла
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found.", status=404)