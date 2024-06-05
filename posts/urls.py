from django.urls import path 
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', AddPostView.as_view(), name='add_post'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('like-comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
