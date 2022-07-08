from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', HomePosts.as_view(), name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('posts/add-post/', add_post, name='add_post'),
    path('test/', test),
]