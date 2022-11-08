from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
from . import views

#ViewSet_and_Routers

router = DefaultRouter()
router.register('articles',ArticleViewSet,basename='articles')
urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.PassengerRegistration.as_view(), name='passenger-registration'),
    path('login/', views.PassengerLogin.as_view(), name='passenger-login'),
    path('logout/', views.Logout.as_view(), name='passenger-logout'),
]


# from .views import article_list, article_details
# from .views import ArticleList,ArticleDetails
# urlpatterns = [
#     path('articles/',ArticleList.as_view()),
#     path('articles/<int:id>/',ArticleDetails.as_view()),
#     path('articles', article_list),
#     path('articles/<int:pk>', article_details),
# ]