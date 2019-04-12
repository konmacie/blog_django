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

from blog_app.models import Post, Comment


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


class CommentAddView(SuccessMessageMixin, CreateView):
    model = Comment
    fields = ['name', 'text']
    success_message = "Comment added successfully!"

    def dispatch(self, request, *args, **kwargs):
        '''
        Overridden to check if selected post exists and is published
        '''
        self.selected_post = get_object_or_404(
            Post, pk=kwargs['post_pk'], status=Post.STATUS_PUBLISHED)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''
        Add selected post to templates context
        '''
        context = super().get_context_data(**kwargs)
        context['post'] = self.selected_post
        return context

    def form_valid(self, form):
        form.instance.post = self.selected_post
        return super().form_valid(form)

    def get_success_url(self):
        return self.selected_post.get_absolute_url()
