from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Slideshow, Slide
from .serializers import SlideshowSerializer, SlideSerializer


@api_view(['GET'])
def root(request, format=None):
    return Response({
        'slideshows': reverse(
            'slideshows', request=request, format=format
        )
    })


class SlideshowList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SlideshowSerializer
    queryset = Slideshow.objects.all()


class SlideList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SlideSerializer

    def get_queryset(self):
        slideshow_id = self.kwargs['slideshow_id']
        return Slide.objects.filter(slideshow=slideshow_id)
