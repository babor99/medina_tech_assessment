"""start_project URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

	path('', views.index),

	# Product Module
	path('product/', include('product.urls.product_urls')),
	path('category/', include('product.urls.category_urls')),
	path('brand/', include('product.urls.brand_urls')),
	path('producttag/', include('product.urls.producttag_urls')),
	path('color/', include('product.urls.color_urls')),
	path('productcolor/', include('product.urls.productcolor_urls')),
	path('size/', include('product.urls.size_urls')),
	path('productsize/', include('product.urls.productsize_urls')),
	path('productimage/', include('product.urls.productimage_urls')),

	# YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

	re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
