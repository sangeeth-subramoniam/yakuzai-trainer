from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'build_weights'
urlpatterns = [
    path('', views.build_weights_home , name = "build_weights_home"),
    path('build_weights_home_initial', views.build_weights_home_initial , name = "build_weights_home_initial"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
