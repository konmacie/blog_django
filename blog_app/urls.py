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
    path('post/new/', views.PostCreateDraftView.as_view(),
         name='post_new'),
    path('post/<int:pk>/manage/', views.PostManageView.as_view(),
         name='post_manage'),
    path('post/<int:pk>/manage/<str:action>/', views.post_action_view,
         name='post_manage_action'),
    path('archive/<int:pk>/', views.ArchiveDetailView.as_view(),
         name='archive_detail'),
    ########################
    # Authentication views #
    ########################
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
