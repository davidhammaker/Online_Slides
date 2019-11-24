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
        """
        Retrieve the temporary URL for the image from Dropbox. This URL
        lasts for 4 hours, and will be used during presentations.
        """

        # Get slideshow ID or return an error
        slideshow_id = self.context['request'] \
            .parser_context['kwargs']['slideshow_id']

        slideshow = Slideshow.objects.filter(id=slideshow_id).first()

        if not slideshow:
            raise serializers.ValidationError(
                'Slideshow does not exist.'
            )

        url = "https://api.dropboxapi.com/2/files/get_temporary_link"
        key = os.environ.get('OSLIDES_DROPBOX_KEY')
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"}
        data = {"path": f"/{slideshow_id}_{slideshow.name}"
                        f"/{slide.image.name.split('/')[-1]}"}
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        pprint(response.json())
        try:
            return response.json()['link']
        except Exception as e:
            return f"error: {e}"

    def validate(self, data):

        # Get slideshow ID or return an error
        slideshow_id = self.context['request'] \
            .parser_context['kwargs']['slideshow_id']

        slideshow = Slideshow.objects.filter(id=slideshow_id).first()

        if not slideshow:
            raise serializers.ValidationError(
                'Slideshow does not exist.'
            )

        # Retrieve the image from posted data
        image = data['image']

        # The image file stored in memory will either be a BytesIO
        # object or a tempfile object. Each must be treated differently.
        if "tempfile" in str(type(image.file)):
            image_data = open(image.file.name, 'rb').read()
        else:
            image_data = image.file.getvalue()

        # Each filetype must be maintained. I don't expect 'bmp' to ever
        # be used, but it has been included just in case.
        extension = 'bmp'
        if image.content_type == 'image/png':
            extension = 'png'
        elif image.content_type == 'image/jpeg':
            extension = 'jpg'

        # The filename is a random number 10-digit number, plus its
        # original file extension.
        filename = f'img{int(899999999*random()) + 100000000}' \
                   f'.{extension}'
        data['image'] = filename

        # The file is uploaded to Dropbox
        url = "https://content.dropboxapi.com/2/files/upload"
        key = os.environ.get('OSLIDES_DROPBOX_KEY')

        dropbox_api_arg = \
            "{\"path\":\"/" + \
            f'{slideshow_id}_{slideshow.name}/{filename}' + "\"}"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": dropbox_api_arg}
        requests.post(url, headers=headers, data=image_data)

        return data