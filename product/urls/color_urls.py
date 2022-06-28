
from django.urls import path
from product.views import color_views as views


urlpatterns = [
	path('api/v1/color/all/', views.getAllColor),

	path('api/v1/color/without_pagination/all/', views.getAllColorWithoutPagination),

	path('api/v1/color/<int:pk>', views.getAColor),
	
	path('api/v1/color/search/', views.searchColor),

	path('api/v1/color/create/', views.createColor),

	path('api/v1/color/delete/<int:pk>', views.deleteColor),

	path('api/v1/color/update/<int:pk>', views.updateColor),

]