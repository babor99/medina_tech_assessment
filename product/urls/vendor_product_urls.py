from django.urls import path
from product.views import vendor_product_views as views



urlpatterns = [

	path('api/v1/vendor_product/all_product_of_individual_vendor/', views.getAllProductOfVendor), #pagination done

	path('api/v1/vendor_product/a_product_of_individual_vendor/<int:pk>', views.getAProductOfVendor),

	path('api/v1/vendor_product/search/', views.searchVendorProduct), #pagination done

	path('api/v1/vendor_product/create/', views.createVendorProduct),

	path('api/v1/vendor_product/update/<int:pk>', views.updateVendorProduct),

	path('api/v1/vendor_product/delete/<int:pk>', views.deleteVendorProduct),

]

