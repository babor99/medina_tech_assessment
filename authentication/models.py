from enum import unique
from django.db import models
from django.db.models.fields import BigAutoField
from django.utils import tree
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField




class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, gender, password=None):
		if not email:
			raise ValueError('User must have an email address')
			
		user = self.model(
			first_name= first_name,
			last_name = last_name,
			email=self.normalize_email(email),
			gender = gender
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, gender, password=None):
		user = self.create_user(
			email= email,
			password=password,
			first_name= first_name,
			last_name = last_name,
			gender = gender
		)
		user.is_admin = True
		user.save(using=self._db)
		return user
 



class User(AbstractBaseUser):
	class Gender(models.TextChoices):
		MALE = 'male', _('Male')
		FEMALE = 'female', _('Female')
		OTHERS = 'others', _('Others')

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100, null=True, blank=True, unique=True)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)

	gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE)

	primary_phone = PhoneNumberField(null=True, blank=True, unique=True)
	secondary_phone = PhoneNumberField(null=True, blank=True, unique=True)

	user_type = models.CharField(max_length=50, null=True, blank=True)

	date_of_birth = models.DateField(null=True, blank=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	address = models.CharField(max_length=255, null=True, blank=True)

	image = models.ImageField(upload_to="users/", null=True, blank=True)
	nid = models.CharField(max_length=32, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	
	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin




class Vendor(User):
	is_online = models.BooleanField(default=True)
	is_company = models.BooleanField(default=False)
	company_name = models.CharField(max_length=200, null=True, blank=True)
	contact_person = models.CharField(max_length=30, null=True, blank=True)

	class Meta:
		ordering = ('-id', )




class CustomerType(models.Model):
	name = models.CharField(max_length=20)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		verbose_name_plural = 'CustomerTypes'
		ordering = ('-id', )

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.capitalize()
		super().save(*args, **kwargs)




class Customer(User):
	is_online = models.BooleanField(default=True)
	customer_type = models.ForeignKey(CustomerType, on_delete=models.SET_NULL, null=True, blank=True)

	class Meta:
		ordering = ('-id', )




