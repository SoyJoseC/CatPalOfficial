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


class MendeleyGroup(models.Model):
    # Mendeley User to handle the group
    mendeley_username = models.CharField(max_length=250)
    mendeley_password = models.CharField(max_length=250)
    # Mendeley Group Id
    mendeley_id = models.CharField(max_length=36)
    name = models.CharField(max_length=250)
    # endeley URL
    link = models.CharField(max_length=250, default='www.mendeley.com')
    # Mendeley Group access type
    access_level = models.CharField(max_length=20, choices=[('private','private'), ('invite_only','invite_only'), ('public','public')], default='private')
    # Documents in the Group.
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return self.name
    pass

