from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', HomePosts.as_view(), name='home'),
    path('category/<int:category_id>/', CategoryPosts.as_view(), name='category'),
    path('posts/add-post/', AddPosts.as_view(), name='add_post'),
    path('test/', test),
]