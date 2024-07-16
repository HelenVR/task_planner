from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, TaskForm, UserLoginForm
from .models import Task


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserLoginForm()
    return render(request, 'tasks/login.html', {'form': form})


def task_list(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if 'register' in request.POST:
                form = UserRegistrationForm(request.POST)
                if form.is_valid():
                    new_user = form.save(commit=False)
                    new_user.set_password(form.cleaned_data['password'])
                    new_user.save()
                    return redirect('login')
            elif 'login' in request.POST:
                form = UserLoginForm(data=request.POST)
                if form.is_valid():
                    user = form.get_user()
                    login(request, user)
                    return redirect('task_list')
        else:
            register_form = UserRegistrationForm()
            login_form = UserLoginForm()
        return render(request, 'tasks/home.html', {'register_form': register_form, 'login_form': login_form})
    else:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def user_logout(request):
    logout(request)
    return redirect('task_list')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Запрашиваемая страница не найдена</h1>")