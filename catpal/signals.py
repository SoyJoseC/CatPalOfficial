# from django.db.models.signals import post_init, post_save
# from django.dispatch import receiver
# from catpal.models import MendeleyGroup,  Category, Document
#
# @receiver(post_save, sender=MendeleyGroup)
# def create_root_category(sender, instance):
#     print('entre')
#     c = Category(name = 'root', group = instance)
#     c.save()
#     print('salvado')