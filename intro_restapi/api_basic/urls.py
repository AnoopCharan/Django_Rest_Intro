from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
app_name= 'api_basic'

# router = DefaultRouter()
# router.register('article', Articles_Viewset, basename='article_viewset')
# router.register('genvs', Articles_GenViewset, basename='article_genericviewset')
# router.register('modelview', Articles_ModelViewset, basename='article_modelviewset')

urlpatterns = [
    # path('list/', article_list),
    # path('list/<int:pk>', article_detail),
    # path('class/list/', Articles_List_APIView.as_view()),
    # path('class/list/<int:pk>',Article_Detail_APIView.as_view()),
    # path('generic/detail/<int:pk>', Articles_Generic_Detail.as_view()),
    # path('generic/list/', Articles_Generic_List.as_view()),
    # path('viewset/', include(router.urls)),
    # path('viewset/<int:pk>', include(router.urls)),
    path('html/', Html_List.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['html', 'json', 'api'])