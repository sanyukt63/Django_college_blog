from django import template
from django.db.models import Count

register = template.Library()

@register.simple_tag(takes_context=True)
def total_posts(context):
    from ..models import Post
    return Post.published.count()

@register.simple_tag(takes_context=True)
def blog_tag(context):
    from ..models import Post
    from django.db.models import Count
    return Post.published.annotate(num_tags=Count('tags')).filter(num_tags__gt=0).count()

