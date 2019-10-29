from django.urls import path, include
from . import views


urlpatterns = [
    path('<int:pk>/new_comment/', views.new_comment),
    path('create/', views.PostCreate.as_view()),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('tag/<str:slug>/', views.PostListByTag.as_view()),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.Postlist.as_view()),
]