from django.urls import path
from . import views as oslides_app_views

urlpatterns = [
    path(
        '',
        oslides_app_views.root,
        name='root'
    ),
    path(
        'slideshows/',
        oslides_app_views.SlideshowList.as_view(),
        name='slideshows'
    ),
    path(
        'slideshows/<int:slideshow_id>/',
        oslides_app_views.SlideList.as_view(),
        name='slides'
    )
]
