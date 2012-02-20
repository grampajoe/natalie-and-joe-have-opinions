from django.contrib import admin
from models import Thing, Opinion

class ThingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class OpinionAdmin(admin.modelAdmin):
    pass

admin.site.register(Thing, ThingAdmin)
admin.site.register(Opinion, OpinionAdmin)
