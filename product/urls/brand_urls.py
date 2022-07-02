
from django.urls import path
from product.views import brand_views as views


urlpatterns = [

	path('api/v1/brand/all/', views.getAllBrand), #pagination done

	path('api/v1/brand/without_pagination/all/', views.getAllBrandWithoutPagination),

	path('api/v1/brand/<int:pk>', views.getABrand),

	path('api/v1/brand/search/', views.searchBrand), #pagination done

	path('api/v1/brand/create/', views.createBrand),

	path('api/v1/brand/update/<int:pk>', views.updateBrand),

	path('api/v1/brand/delete/<int:pk>', views.deleteBrand),

]