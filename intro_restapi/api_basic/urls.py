from django.urls import path
from .views import *
app_name= 'api_basic'

urlpatterns = [
    path('list/', article_list),
    path('list/<int:pk>', article_detail),
    path('class_list/', Articles_List_APIView.as_view()),
    path('class_list/<int:pk>',Article_Detail_APIView.as_view()),
    path('generic_detail/<int:pk>', Articles_Generic_Detail.as_view()),
    path('generic_list/', Articles_Generic_List.as_view())


]