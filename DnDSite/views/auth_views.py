from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from ..forms import CustomAuthenticationForm, CustomUserCreationForm


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')


@login_required
def admin_login_redirect(request):
    if request.user.is_staff:
        return redirect('/admin/')
    else:
        messages.error(request, 'У вас нет прав доступа к админ-панели')
        return redirect('index')