from django.urls import path,include
from . import views
from . import views_scrapped

from django.conf import settings
from django.conf.urls.static import static

app_name = 'build_weights'
urlpatterns = [
    
    path('', views_scrapped.build_weights_home , name = "build_weights_home"),
    # path('build_weights_home_initial', views_scrapped.build_weights_home_initial , name = "build_weights_home_initial"),
    # path('nearest_neighbour', views_scrapped.nearest_neighbour , name = "nearest_neighbour"),
    # path('finding_similar', views_scrapped.finding_similar , name = "finding_similar"),

    path('build_weights_home_initial', views.build_weights_home_initial , name = "build_weights_home_initial"),
    path('similar_images', views.similar_images , name = "similar_images"),
    path('add_single_image', views.add_single_image , name = "add_single_image"),
    
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
