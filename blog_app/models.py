from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse, reverse_lazy

UserModel = get_user_model()


class Post(models.Model):
    # choices for Post.status field
    STATUS_DRAFT, STATUS_PUBLISHED, STATUS_ARCHIVED = range(3)
    _STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived')
    )

    # FIELDS
    author = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,)
    status = models.PositiveSmallIntegerField(
        choices=_STATUS_CHOICES,
        default=STATUS_DRAFT
    )

    title = models.CharField(blank=False, max_length=160)
    text = models.TextField()
    date_pub = models.DateTimeField(
        verbose_name='Publication date',
        default=None,
        blank=True, null=True)
    date_edit = models.DateTimeField(
        verbose_name='Last edited',
        auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')

    name = models.CharField(
        max_length=30,
        blank=False)
    text = models.CharField(
        max_length=250,
        blank=False)
    date_pub = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-date_pub']
