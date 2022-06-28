
from django.urls import path
from product.views import product_views as views


urlpatterns = [

	path('api/v1/product_barcode/', views.getABarcode),

	path('api/v1/product/all/', views.getAllProduct), #pagination done

	path('api/v1/product/without_pagination/all/', views.getAllProductWithoutPagination),

	path('api/v1/product/<int:pk>', views.getAProduct),

	path('api/v1/product_using_category/<int:category_id>', views.getAllProductUsingCategory), #pagination done

	path('api/v1/product_using_category_nested/<int:category_id>', views.getAllProductUsingCategoryNested), #pagination done

	path('api/v1/product_using_brand/<int:brand_id>', views.getAllProductUsingBrand), #pagination done

	path('api/v1/product/search/', views.searchProduct), #pagination done

	path('api/v1/product/filter/', views.filterProduct), #pagination done

	path('api/v1/product/create/', views.createProduct),

	path('api/v1/product/update/<int:pk>', views.updateProduct),

	path('api/v1/product/delete/<int:pk>', views.deleteProduct),

]