from django.contrib import admin
from .models import Contact
# Register your models here.


class ContactAdmin (admin.ModelAdmin):
    list_display = ("firstname", "lastname", "phone", "email")
    search_fields = ("firstname", "lastname")


admin.site.register(Contact, ContactAdmin)
