from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home_page_landing'),
    path('presale_choice/', views.presale_choice, name = 'presale_choice'),
    path('presale_analysis/', views.presale_analysis, name = 'presale_analysis'),
    path('presale_set_up/', views.presale_set_up, name = 'presale_set_up')

]
