from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Count

# Remove broken incomplete tag filter function - post_list works with status filter
def post_list(request, tag_slug=None):
    status_filter = request.GET.get('status')
    tag = None
    posts = Post.objects.filter(status='published').order_by('-publish')
    if status_filter:
        posts = posts.filter(status=status_filter)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/post_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'tag': tag
    })



def post_detail(request, year, month, day, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    # Compute similar posts based on shared tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='published').filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')
                                           ).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    })



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd = None

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['comments']}"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cd['to']], fail_silently=True)
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html', {
        'post': post,
        'form': form,
        'sent': sent,
        'cd': cd
    })

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.active = True
            comment.save()
        form = CommentForm()
    else:
        form = CommentForm()

    return render(request, 'blog/post/comment.html', {
        'post': post,
        'form': form,
        'comment': comment
    })