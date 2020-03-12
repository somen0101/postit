from . import views
from django.urls import path

app_name = 'picture'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:page>', views.index, name='index'),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('tag/<str:tag_name>/<int:page>', views.tag, name='tag'),
    path('search/', views.search_post, name='search'),
    path('search/<str:search_word>', views.search, name='search'),
    path('search/<str:search_word>/<int:page>', views.search, name='search'),
    path('create_post/', views.topic_create, name='create_post'),
    path('detail_post/<int:pk>/', views.TopicAndCommentView.as_view(), name='detail_post')
]