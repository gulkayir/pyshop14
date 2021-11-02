from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from product.views import home_page, product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)