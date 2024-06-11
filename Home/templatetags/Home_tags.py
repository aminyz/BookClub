from django import template
from ..models import Literature, Authors

register = template.Library()


@register.inclusion_tag("partials/latest_post.html")
def latest_posts(count=6):
    l_posts = Literature.published.order_by('-publish_post_time')[:count]
    context = {'l_posts': l_posts}
    return context


@register.inclusion_tag("partials/latest_author.html")
def latest_authors(count=6):
    l_authors = Authors.published.order_by('-created')[:count]
    context = {'l_authors': l_authors}
    return context



