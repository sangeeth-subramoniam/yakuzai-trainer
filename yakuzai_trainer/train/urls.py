from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'train'
urlpatterns = [
    path('', views.train_home , name = "train_home"),
    path('image_post', views.image_post , name = "image_post"),
    path('remove_image', views.remove_image , name = "remove_image"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
