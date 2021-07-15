from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('view_table', views.view_table, name='view_table'),
    path('upload_form', views.upload_form, name='upload_form'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('upload_file_post', views.upload_file),
    path('api/get_top5', views.get_top5),
]
