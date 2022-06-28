from authentication.views import user_views as views
from django.urls import path

urlpatterns = [
	
	path('api/v1/user/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

	path('api/v1/user/all/', views.getAllUser),

	path('api/v1/user/without_pagination/all/', views.getAllUserWithoutPagination),

	path('api/v1/user/<int:pk>', views.getAUser),

	path('api/v1/user/search/', views.searchUser),

	path('api/v1/user/create/', views.createUser),

	path('api/v1/user/update/<int:pk>', views.updateUser),

	path('api/v1/user/delete/<int:pk>', views.deleteUser),

	path('api/v1/user/passwordchange/<int:pk>', views.userPasswordChange),

]
