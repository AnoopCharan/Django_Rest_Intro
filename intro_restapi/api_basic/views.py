from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, request
from django.views.generic.base import View
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import views
from rest_framework import mixins
from rest_framework.parsers import JSONParser
from .models import Articles
from .serializer import Articles_Serializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, renderer_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from rest_framework.mixins import *
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

@api_view(['GET', 'POST']) #extending api_view class
def article_list(request):
    if request.method == 'GET':
        articles= Articles.objects.all()
        serializer = Articles_Serializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = Articles_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Articles.objects.get(pk = pk)
    except Articles.DoesNotExist :
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method== 'GET':
        serializer = Articles_Serializer(article)
        return Response(data= serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = Articles_Serializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class Articles_List_APIView(APIView):
    def get (self, request):
        articles = Articles.objects.all()
        serializer = Articles_Serializer(articles, many=True)
        
        return Response(data=serializer.data)

    def post(self, request):
        post_data_slz = Articles_Serializer(data= request.data)
        

        if post_data_slz.is_valid():
            post_data_slz.save()
            print(f"""
                request: {request} \n
                request.data: {request.data} \n
                post_data_slz: {post_data_slz} \n
                post_data_slz.data :{post_data_slz.data}\n
        
        """)
            
            return Response(post_data_slz.data, status=status.HTTP_201_CREATED)
        return Response(post_data_slz.errors, status=status.HTTP_400_BAD_REQUEST)

class Article_Detail_APIView(APIView):
    # renderer_classes = [JSONRenderer]
    def get_object (self,pk):
        try:
            return Articles.objects.get(pk=pk)
        except Articles.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk):
        if self.get_object(pk):
            article = self.get_object(pk)
        else:
            return
        get_slz = Articles_Serializer(article)
        return Response(get_slz.data)

    def put(self,request, pk):
        article = self.get_object(pk)
        put_slz = Articles_Serializer(instance=article, data=request.data)
        
        if put_slz.is_valid():
            put_slz.save()
            return Response(put_slz.data, status=status.HTTP_202_ACCEPTED)
        return Response(put_slz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Articles_Generic_Detail(GenericAPIView, ListModelMixin, CreateModelMixin,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = Articles_Serializer
    queryset= Articles.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # lookup_field = 'id'

    def get(self, request, pk=None):
        if pk == None:
            return self.list(request)
        elif pk:
            return self.retrieve(request, pk)
    
    def put(self,request, pk=None):
        return self.update(request, pk)
    
    def delete(self,request, pk):
        return self.destroy(request, pk)

class Articles_Generic_List(GenericAPIView, ListModelMixin, CreateModelMixin,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = Articles_Serializer
    queryset= Articles.objects.all()
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # template_name = 'api_basic/articles.html'
    # lookup_field = 'id'
    filterset_fields = ['title','author']
    ordering_fields=['id', 'date']


    def get(self, request):
        print(request.session.session_key)
        return self.list(request)
            
    def post(self,request):
        return self.create(request)


class Articles_Viewset(viewsets.ViewSet):
    def list(self, request):
        articles= Articles.objects.all()
        list_slz = Articles_Serializer(articles, many=True)
        return Response(list_slz.data)

    def create(self, request):
        slz= Articles_Serializer(data=request.data)

        if slz.is_valid():
            slz.save()
            return Response(slz.data, status=status.HTTP_201_CREATED)
        return Response(slz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Articles.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = Articles_Serializer(article)
        return Response(serializer.data)
    
    def update (Self, request, pk=None):
        article = Articles.objects.get(pk=pk)
        upd_slz = Articles_Serializer(instance= article, data=request.data)

        if upd_slz.is_valid():
            upd_slz.save()
            return Response(data = upd_slz.data)
        return Response(data=upd_slz.errors, status= status.HTTP_400_BAD_REQUEST)

class Articles_GenViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = Articles_Serializer
    queryset = Articles.objects.all()
    filters_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

class Articles_ModelViewset(viewsets.ModelViewSet):
    serializer_class = Articles_Serializer
    queryset = Articles.objects.all()
    
    


class Html_List(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]
    template_name='api_basic/articles.html'
    # filters_backends = [DjangoFilterBackend]
    filterset_fields = ['title','author']
    """
    A view that returns a templated HTML representation of a given user.
    """
        
    
    def get(self, request):
        
        queryset= Articles.objects.all()

        get_slz = Articles_Serializer(queryset, many=True)

        return Response(data ={'data':get_slz.data}, status= status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        post_slz = Articles_Serializer(data=data)
        if post_slz.is_valid():
            post_slz.save()        
            return Response({'data': post_slz.data}, status=status.HTTP_201_CREATED)
        return Response({'errors':post_slz.errors },status=status.HTTP_400_BAD_REQUEST)
