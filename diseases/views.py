from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Disease, Symptom
from .forms import RegisterForm  # Твоя кастомна форма з вибором ролі


# ========================
# 1. Головна сторінка та Аналізатор
# ========================
def disease_list(request):
    diseases = Disease.objects.all()
    symptoms = Symptom.objects.all()
    return render(request, 'diseases/index.html', {
        'diseases': diseases,
        'symptoms': symptoms
    })


# ========================
# 2. API для отримання деталей хвороби
# ========================
def disease_detail_api(request, id):
    try:
        # Оптимізований запит із prefetch_related для M2M зв'язків
        disease = Disease.objects.prefetch_related('symptoms').get(id=id)

        symptoms_list = [s.name for s in disease.symptoms.all()]

        data = {
            "name": disease.name,
            "description": disease.description,
            "image": disease.image.url if disease.image else None,
            "symptoms": symptoms_list
        }
        return JsonResponse(data)
    except Disease.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


# ========================
# 3. Реєстрація користувачів
# ========================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            print(f"DEBUG: Юзер {user.username} збережений в базу!")
            messages.success(request, f'Вітаємо, {user.username}!')
            return redirect('login')
        else:
            # Якщо форма невалідна, ми все одно маємо її передати в render з помилками
            print(f"DEBUG: Помилки форми: {form.errors}")
    else:
        # ОБОВ'ЯЗКОВО додаємо цей блок для звичайного відображення сторінки
        form = RegisterForm()

    # Тепер змінна 'form' точно існує в обох випадках
    return render(request, 'register.html', {'form': form})