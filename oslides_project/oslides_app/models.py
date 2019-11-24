from django.db import models


class Slideshow(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Slide(models.Model):
    image = models.ImageField(upload_to="temp_images/")
    slideshow = models.ForeignKey(
        Slideshow,
        on_delete=models.CASCADE,
        related_name='slides'
    )

    def __str__(self):
        return f"{self.slideshow.name} image, {self.id}"
