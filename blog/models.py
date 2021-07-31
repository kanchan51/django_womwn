from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

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
    subtitle = models.CharField(max_length=500)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(blank=True, upload_to='blog_images')

    body=RichTextUploadingField() # add this

    publish=models.DateTimeField(default=timezone.now)
    date_posted = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)