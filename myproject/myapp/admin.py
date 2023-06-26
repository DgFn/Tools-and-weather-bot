from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Дополнительная обработка перед сохранением модели
        super().save_model(request, obj, form, change)

admin.site.register(Plan, PlanAdmin)


# Register your models here.
