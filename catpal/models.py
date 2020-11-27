from django.db import models
from django.urls import reverse

from catpal.utils import generate_hash



# Create your models here.

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

    # Categories in the Group

    def __str__(self):
        return self.name

    def documents(self):
        return self.document_set.all()

    def categories(self):
        return Category.objects.filter(group=self)

    def save(self):
        super().save()
        try:
            c = Category.objects.get(cat_id=self.mendeley_id)
            return
        except Category.DoesNotExist:
            c = Category(name='root', group=self, cat_id=self.mendeley_id)
            c.save()



class Category(models.Model):
    cat_id = models.CharField(max_length=50, unique=True, default=generate_hash)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(MendeleyGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.group.name + ': ' + self.name

    def childs(self):
        """the childs can be refered as category_set"""
        return self.category_set.all()


class Document(models.Model):
    mendeley_id = models.CharField(max_length=100, null=True, unique=True)
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=512)
    websites = models.CharField(max_length=1024, default='')
    abstract = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    groups = models.ManyToManyField(MendeleyGroup)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')




