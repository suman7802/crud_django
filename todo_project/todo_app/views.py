import json
from .models import Todo
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods


def login_required_json(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'You must be authenticated to access this view'}, status=401)
    return _wrapped_view


@csrf_exempt
@require_POST
def user_register(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        form = UserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'message': 'Registration successful'})
        else:
            return JsonResponse({'error': 'Invalid registration details'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'})


@csrf_exempt
@require_POST
def user_login(request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid login credentials'})
        

def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})



@login_required_json
def todo_list(request):
    todos = Todo.objects.all()
    return JsonResponse({'todos': [{'id': todo.id, 'title': todo.title, 'completed': todo.completed} for todo in todos]}, safe=False)


@csrf_exempt
@login_required_json
@require_POST
def add_todo(request):
    data = json.loads(request.body)
    title = data.get('title')
    if title:
        todo = Todo.objects.create(title=title)
        return JsonResponse({'id': todo.id, 'title': todo.title, 'completed': todo.completed})
    else:
        return JsonResponse({'error': 'Missing title'}, status=400)


@csrf_exempt
@login_required_json
@require_http_methods(["PUT"])
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    data = json.loads(request.body)
    title = data.get('title')
    completed = data.get('completed')
    if title is not None:
        todo.title = title
    if completed is not None:
        todo.completed = completed
    todo.save()
    return JsonResponse({'id': todo.id, 'title': todo.title, 'completed': todo.completed})

@csrf_exempt
@login_required_json
@require_http_methods(["DELETE"])
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return JsonResponse({'message': 'Todo deleted successfully'})