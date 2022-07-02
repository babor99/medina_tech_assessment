from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django_currentuser.middleware import get_current_authenticated_user

from product.models import *

User = get_user_model()



def created_by_signals(sender, instance, created, **kwargs):
	if created:
		user = get_current_authenticated_user()
		if user is not None:
			sender.objects.filter(id=instance.id).update(created_by=user)


def updated_by_signals(sender, instance, created, **kwargs):
	if not created:
		user = get_current_authenticated_user()
		if user is not None:
			sender.objects.filter(id=instance.id).update(updated_by=user)



# Brand signals
post_save.connect(created_by_signals, sender=Brand)
post_save.connect(updated_by_signals, sender=Brand)


# Category signals
post_save.connect(created_by_signals, sender=Category)
post_save.connect(updated_by_signals, sender=Category)


# Product signals
post_save.connect(created_by_signals, sender=Product)
post_save.connect(updated_by_signals, sender=Product)


# Discount signals
post_save.connect(created_by_signals, sender=Discount)
post_save.connect(updated_by_signals, sender=Discount)


# Color signals
post_save.connect(created_by_signals, sender=Color)
post_save.connect(updated_by_signals, sender=Color)


# ProductColor signals
post_save.connect(created_by_signals, sender=ProductColor)
post_save.connect(updated_by_signals, sender=ProductColor)


# ProductSize signals
post_save.connect(created_by_signals, sender=ProductSize)
post_save.connect(updated_by_signals, sender=ProductSize)


# ProductImage signals
post_save.connect(created_by_signals, sender=ProductImage)
post_save.connect(updated_by_signals, sender=ProductImage)


