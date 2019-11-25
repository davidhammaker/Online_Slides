from django.contrib import admin
from .models import Slideshow, Slide


class SlideInline(admin.StackedInline):
    model = Slide


class SlideshowAdmin(admin.ModelAdmin):
    fields = [
        'name'
    ]
    inlines = [SlideInline]


admin.site.register(Slideshow, SlideshowAdmin)
