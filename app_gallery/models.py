from django.db import models
import os
from PIL import Image
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import uuid

def picture_file_path(instance, filename):
    """Set the path of the picture with a random filename"""
    extension = os.path.splitext(filename)[1]
    random_filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join('pictures/', random_filename)

def thumbnail_file_path(instance, filename):
    """Set the path of the thumbnail with a random filename"""
    extension = os.path.splitext(filename)[1]
    random_filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join('thumbnails/', random_filename)

class PictureHashtagRelation(models.Model):
    """Union model between Picture and Hashtag"""

    picture = models.ForeignKey('Picture', on_delete=models.CASCADE, related_name='hashtag_relations')
    hashtag = models.ForeignKey('Hashtag', on_delete=models.CASCADE, related_name='picture_relations')

    def __str__(self):
        return f"{self.picture.id} - {self.hashtag.hashtag}"

class Hashtag(models.Model):
    """Hashtag model, many pictures will have many hashtags"""
    hashtag = models.CharField('Etiqueta', max_length=50, unique=True)

    def __str__(self):
        return self.hashtag

class Picture(models.Model):
    """ Picture model, it will have a thumbnail for the masonry view and the original picture for a detailed view """
    image = models.ImageField(upload_to=picture_file_path)
    thumbnail = models.ImageField(upload_to=thumbnail_file_path)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    hashtags = models.ManyToManyField(Hashtag, through=PictureHashtagRelation, blank=True, related_name='pictures')

    def __str__(self):
        """Return the title if it has one"""
        return self.title if self.title else str(self.id)

    def save(self, *args, **kwargs):
        """Check if the picture has thumbnail, in case it doesnt has it will create it"""
        super(Picture, self).save(*args, **kwargs)

        if self.image and not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        """Creates thumbnail"""

        if not self.thumbnail:
            img = Image.open(self.image.path)
            quality = 20   # Set thumbnail quality
            img_copy = img.copy()  # Copy original image
            thumbnail_filename = f"thumbnail_{uuid.uuid4().hex}.jpg"
            thumbnail_path = os.path.join('thumbnails/', thumbnail_filename)
            save_path = os.path.join('media/', thumbnail_path)
            img_copy.save(save_path, quality=quality)
            self.thumbnail = thumbnail_path
            self.save()


@receiver(pre_delete, sender=Picture)
def delete_picture_files(sender, instance, **kwargs):
    # Delete the original file
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    # Delete the thumbnail file
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)