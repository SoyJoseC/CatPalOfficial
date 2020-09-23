from django.db import models
from django.contrib.auth.models import AbstractUser
from catpal.models import MendeleyGroup

"""
Override the User model.
Add groups to the user model."""
class User(AbstractUser):
    #Mendeley2 groups
    groups = models.ManyToManyField(MendeleyGroup)
    #when a MendeleyGroup is selected the User can see the documents belonging to this group.
    current_group = models.ForeignKey(MendeleyGroup, related_name='current_group', on_delete=models.SET_NULL, null=True)

