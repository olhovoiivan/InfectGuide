from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from .models import Disease, Symptom
from .forms import RegisterForm


# ===== ПЕРЕВІРКА ПРАВ ДОСТУПУ (Identity Management) =====
def is_medical_staff(user):
    """Перевіряє, чи є користувач адміністратором або лікарем."""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Doctors').exists())


# 1. ГОЛОВНА СТОРІНКА (Синхронізовано з name='home')
def disease_list(request):
    """Відображає головний термінал зі списком хвороб та аналізатором."""
    diseases = Disease.objects.all().prefetch_related('symptoms')
    symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'diseases/index.html', {
        'diseases': diseases,
        'symptoms': symptoms,
        'is_staff': is_medical_staff(request.user)
    })


# 2. REST API: ДЕТАЛІ ХВОРОБИ (GET)
def disease_detail_api(request, id):
    """Повертає дані про конкретну хворобу у форматі JSON для модального вікна."""
    try:
        disease = Disease.objects.prefetch_related('symptoms').get(id=id)
        data = {
            "id": disease.id,
            "name": disease.name,
            "description": disease.description,
            "image": disease.image.url if disease.image else None,
            "symptoms": [s.name for s in disease.symptoms.all()]
        }
        return JsonResponse(data)
    except Disease.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)


# 3. ДОДАВАННЯ ДАНИХ(POST)
@user_passes_test(is_medical_staff, login_url='login')
def add_disease_view(request):
    """Створює новий запис про хворобу."""
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


# 4. РЕДАГУВАННЯ ДАНИХ (PUT)
@user_passes_test(is_medical_staff, login_url='login')
def edit_disease_view(request, pk):
    """Оновлює існуючий запис у базі даних."""
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == 'POST':
        disease.name = request.POST.get('name')
        disease.description = request.POST.get('description')
        symptom_ids = request.POST.getlist('symptoms')

        if request.FILES.get('image'):
            disease.image = request.FILES.get('image')

        disease.save()
        disease.symptoms.set(symptom_ids)

        messages.success(request, f"Дані '{disease.name}' успішно синхронізовано.")
        return redirect('home')

    all_symptoms = Symptom.objects.all().order_by('name')
    return render(request, 'diseases/edit_disease.html', {
        'disease': disease,
        'all_symptoms': all_symptoms
    })


# 5. ВИДАЛЕННЯ ДАНИХ (DELETE)
@user_passes_test(is_medical_staff, login_url='login')
def delete_disease_view(request, pk):
    """Видаляє запис після підтвердження."""
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == 'POST':
        name = disease.name
        disease.delete()
        messages.warning(request, f"Запис '{name}' видалено з системи.")
        return redirect('home')
    return render(request, 'diseases/confirm_delete.html', {'disease': disease})


# 6. РЕЄСТРАЦІЯ ТА РОЛІ
def register_view(request):
    """Реєструє користувача та призначає групу 'Doctors', якщо обрано відповідну роль."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'doctor':
                group, _ = Group.objects.get_or_create(name='Doctors')
                user.groups.add(group)
                user.is_staff = True
                user.save()
            messages.info(request, "Акаунт створено. Виконайте вхід.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# 7. АНАЛІЗАТОР СИМПТОМІВ (RESTful Filtering)
def check_symptoms(request):
    """Обробляє AJAX-запит від аналізатора та повертає JSON зі списком збігів."""
    symptom_ids = request.GET.getlist('symptoms[]') or request.GET.getlist('symptoms')
    clean_ids = [int(sid) for sid in symptom_ids if sid.isdigit()]

    if not clean_ids:
        return JsonResponse({'diseases': []})

    # Пошук хвороб, що містять хоча б один із обраних симптомів
    diseases = Disease.objects.filter(symptoms__id__in=clean_ids).distinct()
    results = []

    for d in diseases:
        disease_symptom_ids = d.symptoms.values_list('id', flat=True)
        intersection = set(clean_ids) & set(disease_symptom_ids)
        results.append({
            'id': d.id,
            'name': d.name,
            'match_count': len(intersection),
            'tags': [s.name for s in d.symptoms.all()]
        })

    # Сортування: спочатку за кількістю збігів (спадання), потім за назвою (алфавіт)
    results = sorted(results, key=lambda x: (-x['match_count'], x['name']))

    return JsonResponse({'diseases': results})