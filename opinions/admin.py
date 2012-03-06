from django.contrib import admin
from models import Thing, Opinion, Tag

class ThingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class OpinionAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Thing, ThingAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Tag, TagAdmin)
