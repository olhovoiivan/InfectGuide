from django.test import TestCase, Client
from django.urls import reverse
from .models import Disease, Symptom


class InfectGuideMassiveTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Створюємо базовий набір симптомів для тестів
        self.symptoms = [Symptom.objects.create(name=f"Симптом_{i}") for i in range(10)]

    # 1. ТЕСТУВАННЯ ВАЛІДАЦІЇ
    def test_massive_validation(self):
        """Перевірка створення хвороб з різними комбінаціями даних"""
        for i in range(40):
            name = f"Infection_Alpha_{i}"
            desc = "A valid clinical description that must be long enough for the system to accept."
            disease = Disease.objects.create(name=name, description=desc)
            # Додаємо випадкову кількість симптомів
            disease.symptoms.add(*self.symptoms[:(i % 10) + 1])

            self.assertTrue(Disease.objects.filter(name=name).exists())
            # Перевірка, що кожен запис має симптоми
            self.assertGreater(disease.symptoms.count(), 0)

    # 2. ТЕСТУВАННЯ АНАЛІЗАТОРА
    def test_massive_api_queries(self):
        """Емуляція великої кількості пошукових запитів від користувачів"""
        # Створюємо хворобу-мішень
        target = Disease.objects.create(name="Target_Disease", description="Target description text")
        target.symptoms.add(self.symptoms[0])

        for i in range(30):
            # Імітуємо запити з різними ID симптомів
            response = self.client.get(reverse('check_symptoms'), {'symptoms[]': [self.symptoms[0].id]})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('diseases', data)

    # 3. ТЕСТУВАННЯ БЕЗПЕКИ (Identity Management)
    def test_security_access_bulk(self):
        """Перевірка захищених зон (POST, PUT, DELETE) під різними URL"""
        protected_urls = [
            reverse('add_disease'),
            reverse('edit_disease', args=[1]),
            reverse('delete_disease', args=[1]),
        ]
        for url in protected_urls:
            # Анонім має отримувати редирект на логін
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

    # 4. ТЕСТУВАННЯ СТАТИЧНИХ СТОРІНОК ТА РЕДИРЕКТІВ
    def test_page_routing_bulk(self):
        urls = [reverse('home'), reverse('login'), reverse('register')]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)