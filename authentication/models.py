from enum import unique
from django.db import models
from django.db.models.fields import BigAutoField
from django.utils import tree
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField



# models goes here..

class Country(models.Model):
	name = models.CharField(max_length=255)
	capital_name = models.CharField(max_length=255, null=True, blank=True)
	country_code = models.CharField(max_length=255, null=True, blank=True)
	country_code2 = models.CharField(max_length=255, null=True, blank=True)
	phone_code = models.CharField(max_length=255, null=True, blank=True)
	currency_code = models.CharField(max_length=255, null=True, blank=True)
	continent_name = models.CharField(max_length=255, null=True, blank=True)
	continent_code = models.CharField(max_length=255, null=True, blank=True)
	lat = models.IntegerField(null=True, blank=True)
	lon = models.IntegerField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Countries'
		ordering = ('-id',)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.capitalize()
		super().save(*args, **kwargs)




class Permission(models.Model):
	name = models.CharField(max_length=255)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.replace(' ', '_').upper()
		super().save(*args, **kwargs)




class Role(models.Model):
	name = models.CharField(max_length=255)
	permissions = models.ManyToManyField(Permission, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
	
	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.replace(' ', '_').upper()
		super().save(*args, **kwargs)




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

	primary_phone = models.CharField(max_length=20 , null=True, blank=True, unique=True)
	secondary_phone = models.CharField(max_length=20, null=True, blank=True, unique=True)

	user_type = models.CharField(max_length=50, null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	nid = models.CharField(max_length=32, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)

	role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
	postal_code = models.CharField(max_length=50, null=True, blank=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	image = models.ImageField(upload_to="users/", null=True, blank=True)

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

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

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




class Customer(User):
	is_online = models.BooleanField(default=True)

	class Meta:
		ordering = ('-id', )




