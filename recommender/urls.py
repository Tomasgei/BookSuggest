from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Book_Recommender, name = "book_recommender"),
    path("favorite_book/<int:pk>/",views.Book_Detail, name ="book_detail" )
]
