# from django.contrib import admin
# from django.urls import path,include
# from myapp import views
# urlpatterns = [
#     path('', views.index,name='index'),
#     path('analytics', views.analytics,name='analytics'),
#     path('vul', views.vul,name='vul'),
#     path('download', views.download,name='download'),
#     # path('vul', views.search_by_key, name='search_by_key'),

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),  # Direct to analytics
    path('fetch/', views.analytics, name='fetch_data'),  # Hidden endpoint for data refresh
]