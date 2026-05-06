from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Головна сторінка
    path('', views.disease_list, name='home'),

    # 2. Додавання
    path('add/', views.add_disease_view, name='add_disease'),

    # 3. Редагування (ЗМІНЕНО НА _view)
    path('edit/<int:pk>/', views.edit_disease_view, name='edit_disease'),

    # 4. Видалення (ЗМІНЕНО НА _view)
    path('delete/<int:pk>/', views.delete_disease_view, name='delete_disease'),

    # 5. Реєстрація
    path('register/', views.register_view, name='register'),

    # 6. Вхід та Вихід
    path('login/', auth_views.LoginView.as_view(template_name='diseases/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # 7. API
    path('api/disease/<int:id>/', views.disease_detail_api, name='disease_detail_api'),
    path('api/check_symptoms/', views.check_symptoms, name='check_symptoms'),
]