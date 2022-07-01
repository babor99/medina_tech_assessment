from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from django_currentuser.middleware import (get_current_authenticated_user, get_current_user)

from authentication.models import *

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




# City signals
post_save.connect(created_by_signals, sender=City)
post_save.connect(updated_by_signals, sender=City)


# Country signals
post_save.connect(created_by_signals, sender=Country)
post_save.connect(updated_by_signals, sender=Country)


# Vendor signals
post_save.connect(created_by_signals, sender=Vendor)
post_save.connect(updated_by_signals, sender=Vendor)


# Customer signals
post_save.connect(created_by_signals, sender=Customer)
post_save.connect(updated_by_signals, sender=Customer)


# Permission signals
post_save.connect(created_by_signals, sender=Permission)
post_save.connect(updated_by_signals, sender=Permission)


# Role signals
post_save.connect(created_by_signals, sender=Role)
post_save.connect(updated_by_signals, sender=Role)


# user signals
post_save.connect(created_by_signals, sender=User)
post_save.connect(updated_by_signals, sender=User)





