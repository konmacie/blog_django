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


class ArchiveListView(LoginRequiredMixin, ListView):
    '''
    Show archived post. Requires authentication.
    '''
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog_app/archive_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset\
            .filter(status=Post.STATUS_ARCHIVED)\
            .order_by('-date_pub')
        return queryset


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
