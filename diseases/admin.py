from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Disease, Symptom


# ========================
# 1. Proxy-моделі
# ========================
class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Адміністратор'
        verbose_name_plural = '1. Адміністрація системи'
        # Це згрупує їх окремо від хвороб
        app_label = 'auth'


class DoctorUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Лікар'
        verbose_name_plural = '2. Лікарі (Модератори)'
        app_label = 'auth'


class RegularUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Користувач'
        verbose_name_plural = '3. Користувачі(пацієнти/студенти)'
        app_label = 'auth'


# ========================
# 2. Налаштування Admin-класів
# ========================
class BaseUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_main_role', 'is_active')

    def get_main_role(self, obj):
        groups = obj.groups.values_list('name', flat=True)
        return groups[0] if groups else '-'

    get_main_role.short_description = 'Роль'


class AdminUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(groups__name='Адміністрація')


class DoctorUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(groups__name='Лікарі (Модератори)')


class RegularUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(groups__name='Користувачі(пацієнти/студенти)')


# ========================
# 3. Реєстрація
# ========================

# Очищуємо стандартні
admin.site.unregister(User)
admin.site.unregister(Group)

# БЛОК 1: БЕЗПЕКА ТА ДОСТУП (AUTH)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(DoctorUser, DoctorUserAdmin)
admin.site.register(RegularUser, RegularUserAdmin)
# admin.site.register(Group, GroupAdmin)

# БЛОК 2: DISEASES (Твої моделі)
# Ми додаємо verbose_name_plural прямо тут для краси
Symptom._meta.verbose_name_plural = "Симптоми"
Disease._meta.verbose_name_plural = "Хвороби"

admin.site.register(Symptom)
admin.site.register(Disease)

# Глобальні заголовки
admin.site.site_header = "InfectGuide: Control Panel"
admin.site.index_title = "Керування базою знань та доступом"