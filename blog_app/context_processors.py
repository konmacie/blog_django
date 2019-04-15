from .models import Post, Comment


def recent_posts(request):
    '''
    Return 5 most recent Posts with status published
    '''
    posts = Post.objects\
        .filter(status=Post.STATUS_PUBLISHED)\
        .order_by('-date_pub')[:5]
    return {'recent_posts': posts}


def recent_comments(request):
    '''
    Return 5 most recent comments on posts with status published
    '''
    comments = Comment.objects\
        .select_related('post')\
        .filter(post__status=Post.STATUS_PUBLISHED)\
        .order_by('-date_pub')[:5]
    return {'recent_comments': comments}
