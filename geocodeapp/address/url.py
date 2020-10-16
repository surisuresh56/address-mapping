
from django.urls import path,include
from . import views

urlpatterns = [
    path(r'home', views.home,name='home'),
    path(r'upload_excel',views.upload_excel,name='upload_excel'),
    path(r'download_excel', views.download_excel, name='download_excel')
]
