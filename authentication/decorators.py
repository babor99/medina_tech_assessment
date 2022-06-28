from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response




def has_permissions(allowed_permissions=[]):
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			if type(request.user) is not AnonymousUser:
				user = request.user
				role = user.role
				permissions = role.permissions.all()

				if user.is_admin:
					return view_func(request, *args, **kwargs)

				for permission in allowed_permissions:
					if permissions.filter(name=permission).exists():
						# print("Permission =====>", permission)
						return view_func(request, *args, **kwargs)
				else:
					return Response({'detail': f"You don't have these permissions {allowed_permissions}"})
			else:
				return Response({'detail': f"Authentication credentials were not provided."})
		return wrap
	return decorator



def has_role(allowed_role):
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			if type(request.user) is not AnonymousUser:
				user = request.user
				role = user.role

				if role.name == allowed_role:
					return view_func(request, *args, **kwargs)
				else:
					return Response({'detail': f"You don't have these role {allowed_role}"})
			else:
				return Response({'detail': f"Authentication credentials were not provided."})
		return wrap
	return decorator



