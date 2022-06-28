
from django.urls import path
from product.views import size_views as views


urlpatterns = [
	path('api/v1/size/all/', views.getAllSize),

	path('api/v1/size/without_pagination/all/', views.getAllSizeWithoutPagination),

	path('api/v1/size/<int:pk>', views.getASize),
	
	path('api/v1/size/search/', views.searchSize),

	path('api/v1/size/create/', views.createSize),

	path('api/v1/size/update/<int:pk>', views.updateSize),

	path('api/v1/size/delete/<int:pk>', views.deleteSize),
]