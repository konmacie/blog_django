from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import (CreateView, UpdateView, BaseDetailView)
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Post, Comment


class IndexView(ListView):
    '''
    Show posts with STATUS_PUBLISHED
    '''
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter not published posts
        # prefetch Post.author to reduce db queries
        # order by Post.date_pub descending
        queryset = queryset\
            .filter(status=Post.STATUS_PUBLISHED)\
            .select_related('author')\
            .order_by('-date_pub')
        return queryset


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter not published posts
        # prefetch Post.author and related Comments to reduce db queries
        queryset = queryset\
            .filter(status=Post.STATUS_PUBLISHED)\
            .select_related('author')\
            .prefetch_related('comments')
        return queryset


class PostCreateDraftView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    success_message = "Draft created successfully!"

    def form_valid(self, form):
        # set instance's author field to currently logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArchiveDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter not published posts
        # prefetch Post.author and related Comments to reduce db queries
        queryset = queryset\
            .filter(status=Post.STATUS_ARCHIVED)\
            .select_related('author')\
            .prefetch_related('comments')
        return queryset


class PostManageView(UserPassesTestMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog_app/post_manage.html'

    def test_func(self):
        '''
        Check if logged-in user is Post's author
        '''
        post = self.get_object()
        user = self.request.user
        return post.author == user


@login_required
def post_action_view(request, pk, action):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        raise PermissionDenied

    if action == 'publish':
        post.publish()
        messages.add_message(request, messages.SUCCESS,
                             "Post published successfully!")
    elif action == 'archivate':
        post.archivate()
        messages.add_message(request, messages.SUCCESS,
                             "Post archived successfully!")
    elif action == 'republish':
        post.republish()
        messages.add_message(request, messages.SUCCESS,
                             "Post republished successfully!")
    elif action == 'delete':
        post.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Post deleted successfully!")
        return redirect(reverse('index'))
    else:
        messages.add_message(request, messages.ERROR,
                             "Action \"{}\" not found.".format(action))
    return redirect(post.get_absolute_url())
