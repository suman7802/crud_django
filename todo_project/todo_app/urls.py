from django.urls import path
from .views import todo_list, add_todo, update_todo, user_login, user_logout, user_register, delete_todo

urlpatterns = [
    path('todos/', todo_list, name='todo_list'),
    path('todos/add/', add_todo, name='add_todo'),
    path('todos/<int:todo_id>/update/', update_todo, name='update_todo'),
    path('todos/<int:todo_id>/delete/', delete_todo, name='delete_todo'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
