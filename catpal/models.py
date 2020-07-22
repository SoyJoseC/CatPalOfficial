from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Document(models.Model):
    id_mendeley = models.CharField(max_length=100, null=True, unique=True)
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=512)
    abstract = models.TextField(null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

