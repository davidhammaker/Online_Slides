import os
import json
from random import random
from rest_framework import serializers
import requests
from .models import Slideshow, Slide

from pprint import pprint


class SlideshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slideshow
        fields = [
            'id',
            'name'
        ]


class SlideSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        write_only=True,
    )
    image_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = [
            'id',
            'slideshow',
            'image',
            'image_name',
            'image_url'
        ]

    def get_image_name(self, slide):
        return slide.image.name.split('/')[-1]

    def get_image_url(self, slide):
        url = "https://api.dropboxapi.com/2/files/get_temporary_link"
        key = os.environ.get('OSLIDES_DROPBOX_KEY')
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"}
        data = {"path": f"/{slide.image.name.split('/')[-1]}"}
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        return response.json()['link']

    def validate(self, data):
        slideshow_id = self.context['request'] \
            .parser_context['kwargs']['slideshow_id']

        slideshow = Slideshow.objects.filter(id=slideshow_id).first()

        if not slideshow:
            raise serializers.ValidationError(
                'Slideshow does not exist.'
            )

        image = data['image']
        pprint(image.__dict__)
        print(str(type(image.file)))
        if "tempfile" in str(type(image.file)):
            image_data = open(image.file.name, 'rb').read()
        else:
            image_data = image.file.getvalue()
        extension = 'bmp'
        if image.content_type == 'image/png':
            extension = 'png'
        elif image.content_type == 'image/jpeg':
            extension = 'jpg'
        filename = \
            f'img{int(899999999*random()) + 100000000}.{extension}'
        data['image'] = filename
        print('DATA\nDATA\nDATA')
        pprint(data)
        url = "https://content.dropboxapi.com/2/files/upload"
        key = os.environ.get('OSLIDES_DROPBOX_KEY')
        dropbox_api_arg = "{\"path\":\"/" + f'{filename}' + "\"}"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": dropbox_api_arg}
        response = requests.post(url, headers=headers, data=image_data)
        print(response.json())
        return data