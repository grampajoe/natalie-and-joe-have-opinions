from django.contrib import admin
from models import Thing, Opinion, Versus, VersusOpinion

class OpinionInline(admin.StackedInline):
    model = Opinion
    max_num = 2

class ThingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('rating', 'unity')
    inlines = [
        OpinionInline,
            ]
    search_fields = ['name']

class VersusOpinionInline(admin.StackedInline):
    model = VersusOpinion
    max_num = 2

class VersusAdmin(admin.ModelAdmin):
    inlines = [
        VersusOpinionInline,
            ]
    search_fields = ['thing_one__name', 'thing_two__name']

admin.site.register(Thing, ThingAdmin)
admin.site.register(Versus, VersusAdmin)
