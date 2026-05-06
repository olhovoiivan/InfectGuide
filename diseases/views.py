import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Disease, Symptom
from .forms import RegisterForm

# ==========================================
# 1. Identity Management (Перевірка прав)
# ==========================================

def is_medical_staff(user):
    """Доступ для адміністраторів або групи 'Лікарі (Модератори)'."""
    return user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name='Лікарі (Модератори)').exists()
    )


def can_delete_infect(user):
    """Гранулярний контроль: право саме на видалення ресурсу."""
    return user.is_authenticated and (
            user.is_superuser or
            user.has_perm('diseases.delete_disease')
    )

# ==========================================
# 2. Сторінки інтерфейсу (Render)
# ==========================================

def disease_list(request):
    """Головна сторінка: каталог (Grid) та аналізатор."""
    diseases = Disease.objects.all().prefetch_related('symptoms')
    symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'diseases/index.html', {
        'diseases': diseases,
        'symptoms': symptoms,
        'is_staff': is_medical_staff(request.user),
        'can_delete': can_delete_infect(request.user)
    })

@user_passes_test(is_medical_staff, login_url='login')
def add_disease_view(request):
    """Створення нового запису (POST)."""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        symptom_ids = request.POST.getlist('symptoms')

        disease = Disease.objects.create(name=name, description=description, image=image)
        if symptom_ids:
            disease.symptoms.set(symptom_ids)

        messages.success(request, f"Запис '{name}' успішно додано до бази.")
        return redirect('home')

    all_symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'diseases/add_disease.html', {'symptoms': all_symptoms})

# ==========================================
# 3. RESTful API Endpoints (JSON / PUT / DELETE)
# ==========================================

@require_http_methods(["GET"])
def disease_detail_api(request, id):
    """GET: Повертає дані про хворобу для модального вікна (Stateless)."""
    try:
        disease = Disease.objects.prefetch_related('symptoms').get(id=id)
        return JsonResponse({
            "id": disease.id,
            "name": disease.name,
            "description": disease.description,
            "image": disease.image.url if disease.image else None,
            "symptoms": [s.name for s in disease.symptoms.all()]
        }, status=200)
    except Disease.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


@csrf_exempt
@user_passes_test(is_medical_staff)
def edit_disease_view(request, pk):
    """Гібридний метод: GET (форма) та PUT/POST (оновлення)."""
    disease = get_object_or_404(Disease, pk=pk)
    # Обробка оновлення (REST PUT або Form POST)
    if request.method in ['POST', 'PUT']:
        if request.headers.get('Content-Type') == 'application/json' or request.method == 'PUT':
            # Обробка JSON запиту (PUT)
            data = json.loads(request.body)
            disease.name = data.get('name', disease.name)
            disease.description = data.get('description', disease.description)
            disease.save()
            return JsonResponse({"message": "Updated via PUT successful"}, status=200)
        else:
            # Обробка стандартної форми (POST)
            disease.name = request.POST.get('name')
            disease.description = request.POST.get('description')
            if request.FILES.get('image'):
                disease.image = request.FILES.get('image')
            disease.save()
            disease.symptoms.set(request.POST.getlist('symptoms'))
            messages.success(request, f"Дані '{disease.name}' оновлено.")
            return redirect('home')

    # Відображення форми (GET) - це виправить помилку зі скріншота image_584dfd.png
    all_symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'diseases/edit_disease.html', {
        'disease': disease, 'all_symptoms': all_symptoms
    })


@csrf_exempt
@user_passes_test(can_delete_infect)
def delete_disease_view(request, pk):
    """Гібридний метод: GET (підтвердження) та DELETE/POST (видалення)."""
    disease = get_object_or_404(Disease, pk=pk)

    if request.method in ['POST', 'DELETE']:
        name = disease.name
        disease.delete()
        if request.method == 'DELETE':
            return JsonResponse({"message": "Deleted via DELETE successful"}, status=204)
        messages.warning(request, f"Запис '{name}' видалено.")
        return redirect('home')

    return render(request, 'diseases/confirm_delete.html', {'disease': disease})

# ==========================================
# 4. Аналізатор та Реєстрація
# ==========================================

def check_symptoms(request):
    """REST API: Обробляє AJAX-запит аналізатора симптомів."""
    symptom_ids = request.GET.getlist('symptoms[]') or request.GET.getlist('symptoms')
    clean_ids = [int(sid) for sid in symptom_ids if sid.isdigit()]

    if not clean_ids:
        return JsonResponse({'diseases': []}, status=200)

    diseases = Disease.objects.filter(symptoms__id__in=clean_ids).distinct().prefetch_related('symptoms')
    results = []

    for d in diseases:
        intersect = set(clean_ids) & set(d.symptoms.values_list('id', flat=True))
        results.append({
            'id': d.id,
            'name': d.name,
            'match_count': len(intersect),
            'tags': [s.name for s in d.symptoms.all()]
        })

    results = sorted(results, key=lambda x: (-x['match_count'], x['name']))
    return JsonResponse({'diseases': results}, status=200)


def register_view(request):
    """Реєстрація користувача."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Акаунт створено. Очікуйте підтвердження ролі адміністратором.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

