from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=user, password=password)

    if not user:
        messages.error(request, 'user or password invalid')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'logged')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    repeatpassword = request.POST.get('repeatpassword')
    if not name or not surname or not email or not user or not password \
            or not repeatpassword:
        messages.error(request, 'empty')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'error in email')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'error password')
        return render(request, 'accounts/register.html')
    if password != repeatpassword:
        messages.error(request, 'error password')
        return render(request, 'accounts/register.html')

    messages.success(request, 'successfully registered')
    user = User.objects.create_user(username=user, email=email, password=password,
                                    first_name=name, last_name=surname)
    user.save()
    return redirect(login)


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'dashboard/login.html', {'form': form})
    form = FormContact(request.POST, request.FILE)

    if not form.is_valid():
        messages.error(request, 'Erro')
        form = FormContact(request.POST)
        return render(request, 'dashboard/login.html', {'form': form})
