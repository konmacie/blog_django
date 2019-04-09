from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied

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
        blank=True, null=True)
    date_edit = models.DateTimeField(
        verbose_name='Last edited',
        auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        if self.status == Post.STATUS_DRAFT:
            return reverse('post_manage', kwargs={'pk': self.pk})
        elif self.status == Post.STATUS_ARCHIVED:
            return reverse('archive_detail', kwargs={'pk': self.pk})

        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_status(self):
        '''
        Return status as string from Post._STATUS_CHOICES
        '''
        return self._STATUS_CHOICES[self.status][1]

    def __str__(self):
        return str(self.title)

    ################################
    # Actions for post_action_view #
    ################################
    def publish(self):
        if self.status != Post.STATUS_DRAFT:
            raise PermissionDenied
        self.status = Post.STATUS_PUBLISHED
        self.date_pub = timezone.now()
        self.save()

    def archivate(self):
        if self.status != Post.STATUS_PUBLISHED:
            raise PermissionDenied
        self.status = Post.STATUS_ARCHIVED
        self.save()

    def republish(self):
        if self.status != Post.STATUS_ARCHIVED:
            raise PermissionDenied
        self.status = Post.STATUS_PUBLISHED
        self.save()


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

    def __str__(self):
        return str(self.name) + " (" + str(self.date_pub) + ")"
