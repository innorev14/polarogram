from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('liked/<int:post_id>/', PostLiked.as_view(), name='liked'),
    path('saved/<int:post_id>/', PostSaved.as_view(), name='saved'),
    path('create/', PostCreate.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('like/', PostLikedList.as_view(), name='liked_list'),
    path('save/', PostSavedList.as_view(), name='saved_list'),
    path('', PostList.as_view(), name='index'),
]
