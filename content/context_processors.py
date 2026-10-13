from .models import Tag
from django.db.models import Count, Q

def popular_tags(request):
    tags = (
        Tag.objects
        .annotate(num_articles=Count('articles', filter=Q(articles__is_published=True)))
        .order_by('-num_articles', 'name')[:20]
    )
    return {'popular_tags': tags}
