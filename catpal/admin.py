from django.contrib import admin
from catpal.models import Document,Category, MendeleyGroup
# Register your models here.
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(MendeleyGroup)

