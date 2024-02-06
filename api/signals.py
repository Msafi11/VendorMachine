from django.dispatch import receiver, Signal
from api import models
from django.db.models.signals import post_save, pre_delete
from api.models import CustomUser, Product
from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging
from django.contrib.auth import get_user_model


deposit_made = Signal()
buy_made = Signal()
reset_deposit_made = Signal()
product_added = Signal()
product_updated = Signal()
product_deleted = Signal()

logger = logging.getLogger('user_actions')

@receiver(post_save, sender=models.CustomUser)
def buyer_seller_signal_handler(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'buyer':
            buyer = models.Buyer(custom_user=instance)
            buyer.save()
        elif instance.role == 'seller':
            seller = models.Seller(custom_user=instance)
            seller.save()


@receiver(post_save, sender=CustomUser)
def log_user_signup(sender, instance, created, **kwargs):
    if created:
        user_type = instance.role
        logger.info(f"User signed up: {instance.username} ({user_type})")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username} ({user.role})")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username} ({user.role})")





