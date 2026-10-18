from django.contrib import admin
from .models import Pregunta, Opcion


class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 2


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('pregunta_texto', 'pub_date')
    search_fields = ['pregunta_texto']
    inlines = [OpcionInline]


admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Opcion)
