from django.urls import path
from . import views


urlpatterns = [
  path('', views.addSampleData),
  path('user_list/', views.UserList),
  path('tweet_list/', views.TweetList),


  path('user/', views.createUser),
  path('tweet/', views.createTweet),
  path('user/<str:id>/feed/', views.getTweetFeed),
]