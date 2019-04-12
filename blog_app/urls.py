from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    ##############
    # Blog views #
    ##############
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('post/<int:post_pk>/comment', views.CommentAddView.as_view(),
         name='comment_add'),
    #################################
    # Urls requiring authentication #
    #################################
    path('post/new/', views.PostCreateDraftView.as_view(),
         name='post_new'),
    path('post/<int:pk>/manage/', views.PostManageView.as_view(),
         name='post_manage'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(),
         name='post_edit'),
    path('post/<int:pk>/manage/<str:action>/', views.post_action_view,
         name='post_manage_action'),
    path('my-posts/', views.UserPostList.as_view(),
         name='user_posts', kwargs={'status': 'published'}),
    path('my-posts/<str:status>/', views.UserPostList.as_view(),
         name='user_posts_status'),
    path('archive/', views.ArchiveListView.as_view(),
         name='archive_list'),
    path('archive/<int:pk>/', views.ArchiveDetailView.as_view(),
         name='archive_detail'),
    ########################
    # Authentication views #
    ########################
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
