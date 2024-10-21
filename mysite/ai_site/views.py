import cv2
import torch
from django.contrib.auth import authenticate, login
from django.core.files.storage import default_storage
from .forms import RegistrationForm, LoginForm, ImageUploadForm
from django.templatetags.static import static
from django.utils import timezone
import pytz


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['username'] = user.username
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username  # Сохранение имени пользователя в сессии
                return redirect('home')
            else:
                form.add_error('username', 'Неверное имя пользователя или пароль')
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from .models import EditHistory
from django.core.files.storage import FileSystemStorage


def editor_view(request, image_path=None):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        image_name = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(image_name)

        if request.user.is_authenticated:
            EditHistory.objects.create(
                user=request.user,
                image_name=uploaded_image.name,
                edited_image_path=image_url
            )
    elif image_path:
        image_url = image_path
    else:
        image_url = None

    default_image_url = static('default_image.jpg')

    return render(request, 'editor.html', {'image_url': image_url, 'default_image_url': default_image_url})

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def detect_objects(image_path):
    results = model(image_path)
    results.render()
    return results


def image_upload(request):
    image_url = None
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        uploaded_image = form.cleaned_data['image']

        image_path = default_storage.save(uploaded_image.name, uploaded_image)
        image_path_full = default_storage.path(image_path)

        results = detect_objects(image_path_full)
        annotated_image = results.ims[0]
        annotated_image_path = f"media/annotated_{uploaded_image.name}"
        cv2.imwrite(annotated_image_path, annotated_image)
        image_url = f"/{annotated_image_path}"
    else:
        if request.method == 'POST':
            print("Form is not valid:", form.errors)

    return render(request, 'upload.html', {'form': form, 'image_url': image_url})


def edit_history_view(request):
    if request.user.is_authenticated:
        history = EditHistory.objects.filter(user=request.user).order_by('-timestamp')

        for edit in history:
            edit.timestamp = timezone.localtime(edit.timestamp, timezone=pytz.timezone('Europe/Moscow'))
        return render(request, 'edit_history.html', {'history': history})
    else:
        return redirect('login')
