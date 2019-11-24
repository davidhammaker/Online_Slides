from django.contrib import admin
from .models import Slideshow


class SlideshowAdmin(admin.ModelAdmin):
    fields = [
        'name'
    ]


admin.site.register(Slideshow, SlideshowAdmin)
