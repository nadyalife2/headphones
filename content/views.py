from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Article, Tag, Comparison


def home(request):
    popular_tags = (
        Tag.objects
        .annotate(num_articles=Count('articles', filter=Q(articles__is_published=True)))
        .order_by('-num_articles', 'name')[:20]
    )

    # Последние материалы для карточек на главной
    latest_news = Article.objects.filter(category='news').order_by('-created_at')[:5]

    all_news = Article.objects.filter(category='news').order_by('-created_at')
    paginator_news = Paginator(all_news, 5)
    page_number_news = request.GET.get('page_news')
    page_obj_news = paginator_news.get_page(page_number_news)

    # Пагинация обзоров
    all_reviews = Article.objects.filter(is_published=True, category='review').order_by('-created_at')
    paginator_reviews = Paginator(all_reviews, 3)
    page_number_reviews = request.GET.get('page_reviews')
    page_obj_reviews = paginator_reviews.get_page(page_number_reviews)

    # Пагинация сравнений (новая модель)
    all_comparisons = Comparison.objects.filter(is_published=True).order_by('-created_at')
    paginator_comparisons = Paginator(all_comparisons, 1)
    page_number_comparisons = request.GET.get('page_comparisons')
    page_obj_comparisons = paginator_comparisons.get_page(page_number_comparisons)

    context = {
        'latest_news': latest_news,
        'page_obj_news': page_obj_news,
        'page_obj_reviews': page_obj_reviews,
        'page_obj_comparisons': page_obj_comparisons,
        'popular_tags': popular_tags,
        'current_category': 'home',
    }
    return render(request, 'home.html', context)


def comparison_list(request):
    # Получаем все опубликованные сравнения
    comparisons = Comparison.objects.filter(is_published=True)

    # Поиск
    q = request.GET.get('q')
    if q:
        comparisons = comparisons.filter(
            Q(title__icontains=q) |
            Q(model1_name__icontains=q) |
            Q(model2_name__icontains=q)
        )

    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort in ['-created_at', 'created_at', 'title']:
        comparisons = comparisons.order_by(sort)
    else:
        comparisons = comparisons.order_by('-created_at')

    # Пагинация
    paginator = Paginator(comparisons, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comparison_list.html', {
        'page_obj': page_obj,
        'page_title': 'Сравнения',
        'q': q,
        'current_sort': sort,
        'current_category': 'comparison',
    })


def comparison_detail(request, slug):
    comparison = get_object_or_404(Comparison, slug=slug, is_published=True)

    # Получаем похожие сравнения по тегам
    related_comparisons = Comparison.objects.filter(
        tags__in=comparison.tags.all(),
        is_published=True
    ).exclude(id=comparison.id).distinct()

    # Получаем параметры сортировки
    sort = request.GET.get('sort', '-created_at')

    # Проверка валидности сортировки
    if sort in ['-created_at', 'created_at', 'title']:
        related_comparisons = related_comparisons.order_by(sort)
    else:
        related_comparisons = related_comparisons.order_by('-created_at')

    # Ограничиваем количество
    related_comparisons = related_comparisons[:6]

    return render(request, 'comparison_detail.html', {
        'comparison': comparison,
        'related_comparisons': related_comparisons,
        'current_sort': sort
    })


def models_list(request):
    models_cards = Article.objects.filter(is_published=True)
    return render(request, 'models.html', {'models_cards': models_cards})


def category_articles(request, category):
    allowed = {'news', 'review', 'comparison'}
    if category not in allowed:
        return render(request, 'category_not_found.html', status=404)

    q = request.GET.get('q', '').strip()
    qs = Article.objects.filter(is_published=True, category=category)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))

    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by not in ['-created_at', 'created_at', 'title']:
        sort_by = '-created_at'

    # Применяем сортировку
    qs = qs.order_by(sort_by)

    paginator = Paginator(qs, 7)
    page_obj = paginator.get_page(request.GET.get('page'))

    popular_tags = Tag.objects.filter(articles__is_published=True).distinct()[:20]

    category_titles = {
        'news': 'Новости',
        'review': 'Обзоры',
        'comparison': 'Сравнения'
    }
    page_title = category_titles.get(category, category.capitalize())

    return render(request, 'category_list.html', {
        'articles': page_obj.object_list,
        'page_obj': page_obj,
        'category': category,
        'page_title': page_title,
        'q': q,
        'popular_tags': popular_tags,
        'current_sort': sort_by,
        'current_category': category,
    })


def tag_list(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    # Получаем параметры сортировки и поиска
    sort = request.GET.get('sort', '-created_at')
    query = request.GET.get('q', '')

    # Получаем статьи и сравнения
    articles = Article.objects.filter(tags=tag, is_published=True)
    comparisons = Comparison.objects.filter(tags=tag, is_published=True)

    # Фильтрация по поиску
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        comparisons = comparisons.filter(
            Q(title__icontains=query) | Q(model1_name__icontains=query) | Q(model2_name__icontains=query)
        )

    # Проверка валидности сортировки
    if sort not in ['-created_at', 'created_at', 'title']:
        sort = '-created_at'

    # Создаем общий список с типами
    combined_list = []

    # Добавляем статьи
    for article in articles.order_by(sort):
        combined_list.append({
            'object': article,
            'type': 'article',
            'created_at': article.created_at,
            'title': article.title
        })

    # Добавляем сравнения
    for comparison in comparisons.order_by(sort):
        combined_list.append({
            'object': comparison,
            'type': 'comparison',
            'created_at': comparison.created_at,
            'title': comparison.title
        })

    # Сортируем общий список
    if sort == '-created_at':
        combined_list.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort == 'created_at':
        combined_list.sort(key=lambda x: x['created_at'])
    elif sort == 'title':
        combined_list.sort(key=lambda x: x['title'])

    # Пагинация
    paginator = Paginator(combined_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Популярные теги
    popular_tags = (
        Tag.objects
        .annotate(num_articles=Count('articles', filter=Q(articles__is_published=True)))
        .order_by('-num_articles', 'name')[:20]
    )

    return render(request, 'tag_list.html', {
        'tag': tag,
        'current_tag_slug': slug,
        'page_obj': page_obj,
        'page_title': f'Статьи по тегу: {tag.name}',
        'current_sort': sort,
        'q': query,
        'popular_tags': popular_tags,
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'article_detail.html', {'article': article})


def privacy(request):
    return render(request, 'privacy.html')


def agreement(request):
    return render(request, 'agreement.html')
