from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration_form'),
    path('profile/<int:pk>/update/', views.MyProfileUpdate.as_view(), name='profile_update'),
    path('posts/', views.PostList.as_view(), name='posts_list'),
    path('post/<int:pk>/create/', views.PostCreate.as_view(), name='post_create_form'),
    path('post/<int:pk>/details', views.PostView.as_view(), name='post_details'),
    path('profile/<int:pk>/info/', views.AuthorDetail.as_view(), name='author_info'),
    path('profile/<int:pk>/my_posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('profile/<int:pk>/post_update/', views.MyPostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/all_comments/', views.CommentsList.as_view(), name='comments_list'),
    path('feedback/', views.FeedbackView.as_view(), name='send_feedback'),
]
