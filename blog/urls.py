from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.Postlist.as_view()),
]