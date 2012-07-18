from django.contrib import admin
from django import forms
from models import Thing, Opinion, Versus, VersusOpinion, Picture

class OpinionInline(admin.StackedInline):
    model = Opinion
    max_num = 2

class PictureInline(admin.TabularInline):
    model = Picture
    fields = ('image', 'description', 'label')

class ThingForm(forms.ModelForm):
    image = forms.ImageField(help_text="Minimum 780px wide.")

    class Meta:
        model = Thing

class ThingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('rating', 'unity')
    inlines = [
        OpinionInline,
        PictureInline,
            ]
    search_fields = ['name']
    form = ThingForm

class VersusOpinionInline(admin.StackedInline):
    model = VersusOpinion
    max_num = 2

class VersusAdmin(admin.ModelAdmin):
    inlines = [
        VersusOpinionInline,
        PictureInline,
            ]
    search_fields = ['thing_one__name', 'thing_two__name']

admin.site.register(Thing, ThingAdmin)
admin.site.register(Versus, VersusAdmin)
