from django.shortcuts import render, HttpResponse
from requests import delete
from rest_framework.views import APIView
from .models import Article, Passenger
from .serializers import ArticleSerializer,LoginSerializer,RegistrationSerializer
from django.http  import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



#ModelViewSet
from rest_framework import viewsets
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer 


class PassengerRegistration(APIView):
    """
    Register a Passenger

    """
    serializer_class = RegistrationSerializer

    def get(self, request, format=None):
        customers = Passenger.objects.all()
        serializer = RegistrationSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerLogin(APIView):

    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            request.session['passenger_id'] = serializer.validated_data["passenger_id"]
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def get(self, request, format=None):
        del request.session['passenger_id']
        data = {'Logout': 'logged out successfully'}
        return Response(data, status=status.HTTP_200_OK)


'''
#Generic_viewset

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



#Viewset_ased_view

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

class ArticleViewSet(viewsets.ViewSet):
    def list(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self,request,pk=None):
        article = Article.objects.get(pk=pk)

        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Generic_based_view

from rest_framework import generics
from rest_framework import mixins
class ArticleList(generics.GenericAPIView,mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset         = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class ArticleDetails(generics.GenericAPIView,mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset         = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

    def get(self,request,id):
        return self.retrieve(request, id=id)

    def put(self,request,id):
        return self.update(request,id=id)

    def delete(self,request,id):
        return self.destroy(request,id=id)



#Class_based_views

from rest_framework.decorators import APIView
class ArticleList(APIView):

    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#function_base_view

@api_view(['GET','POST'])
def article_list(request):
    #get all articles
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_details(request,pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
'''