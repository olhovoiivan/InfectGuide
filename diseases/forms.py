from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


# Ми використовуємо стандартну форму Django для створення юзера,
# але розширюємо її своїми полями.
class RegisterForm(UserCreationForm):
    # Додаємо поле пошти (воно обов'язкове)
    email = forms.EmailField(required=True, label="Електронна пошта")

    # Створюємо вибір ролей для твого медичного сайту
    ROLE_CHOICES = (
        ('user', 'Студент / Пацієнт'),
        ('doctor', 'Лікар (потребує модерації)'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Хто ви?")

    class Meta(UserCreationForm.Meta):
        model = User
        # Вказуємо, які поля показувати у формі (паролі додадуться автоматично)
        fields = ('username', 'email')

    # Цей метод спрацює, коли користувач натисне кнопку "Зареєструватись"
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Логіка розподілу по групах, які ми раніше налаштували в адмінці
            role = self.cleaned_data.get('role')
            try:
                if role == 'doctor':
                    group = Group.objects.get(name='Лікарі (Модератори)')
                else:
                    group = Group.objects.get(name='Користувачі(пацієнти/студенти)')

                user.groups.add(group)
            except Group.DoesNotExist:
                # На випадок, якщо групи в базі ще не створені
                pass
        return user

    