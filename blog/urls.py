from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeBlogView.as_view(), name='home'),
    # path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),

]

urlpatterns += [
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
]

urlpatterns += [
    path('contact/', views.contact_us, name='contact-us')
]