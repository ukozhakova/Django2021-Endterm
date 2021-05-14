from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from .models import *
import logging

logger = logging.getLogger('api')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile for user {instance} was created")
        logger.info(f"Profile for user {instance} was created")

def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print(f"Profile for user {instance} was saved")
    logger.info(f"Profile for user {instance} was created")

post_save.connect(save_profile, sender = User)

@receiver(post_save, sender=Provider)
def provider_created(sender, instance, created, **kwargs):
    if created:
        print(f'New provider {instance} was created')

@receiver(pre_delete, sender = Category)
def handle_deleted_category(**kwargs):
    category = kwargs['instance']
    products = Product.objects.filter(category= category)
    for _ in products:
        message = "Category {} with products {} - {} has been deleted".format(category.name, _.name, _.price)
        print(message)
        logger.info(message)
        logger.debug(message)

@receiver(pre_delete, sender = Provider)
def handle_deleted_provider(**kwargs):
    provider = kwargs['instance']
    products = Product.objects.filter(provider= provider)
    for _ in products:
        message = "Provider {} with products {} - {} has been deleted".format(provider.name, _.name, _.price)
        print(message)
        logger.info(message)
        logger.debug(message)