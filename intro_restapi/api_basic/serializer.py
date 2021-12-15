from django.db import models
from rest_framework import serializers
from .models import Articles
from django.contrib.auth.models import User, Group


# class Articles_Serializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)
#     date = serializers.DateField()
    
#     # create 
#     def create(self, validated_data):
#         return Articles.objects.create(validated_data)

#     # update
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.author= validated_data.get('author', instance.author)
#         instance.email = validated_data.get('email', instance.email)
#         instance.date = validated_data.get('date', instance.date)
#         instance.save()

#         return instance


class Articles_Serializer(serializers.ModelSerializer):
    """
    pass in model query data, !add 'many=True' when passing queryset"""

    class Meta:
        model = Articles
        # fields=['id', 'title', 'author','email']
        fields= '__all__'
