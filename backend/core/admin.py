from django.contrib import admin
from .models import Organization, Branch, Role

admin.site.register(Organization)
admin.site.register(Branch)
admin.site.register(Role)