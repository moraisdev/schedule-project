from django.contrib import admin
from .models import Category, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email',
                    'creation_date', 'display')
    list_per_page = 10
    search_fields = ('name', 'surname', 'phone', 'email')
    list_editable = ('phone', 'display')


admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
