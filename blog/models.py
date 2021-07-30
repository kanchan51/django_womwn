from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from django.urls import reverse
from tinymce.models import HTMLField

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, 
            self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    content = models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    date_posted = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="name of sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return (self.name, "-", self.email)