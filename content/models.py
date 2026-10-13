# content/models.py
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('review', 'Обзоры'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    cover = models.ImageField(upload_to='articles/covers/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO поля
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ArticleBlock(models.Model):
    HEADING_CHOICES = [
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
    ]

    IMAGE_SIZE_CHOICES = [
        ('original', 'Оригинальный'),
        ('square', 'Квадрат (1:1)'),
        ('vertical', 'Вертикальный (1:2)'),
        ('horizontal', 'Горизонтальный (2:1)'),
    ]

    TEXT_POSITION_CHOICES = [
        ('left', 'Слева'),
        ('right', 'Справа'),
    ]

    article = models.ForeignKey(Article, related_name='blocks', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    # Текстовые поля
    heading_type = models.CharField(max_length=5, choices=HEADING_CHOICES, blank=True)
    heading_text = models.CharField(max_length=200, blank=True)
    text_content = RichTextUploadingField(blank=True)
    text_position = models.CharField(max_length=10, choices=TEXT_POSITION_CHOICES, default='right')

    # Изображение
    image = models.ImageField(upload_to='articles/blocks/', blank=True, null=True)
    image_size = models.CharField(max_length=20, choices=IMAGE_SIZE_CHOICES, default='horizontal')
    image_alt_text = models.CharField(max_length=200, blank=True)
    image_title = models.CharField(max_length=200, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок статьи'
        verbose_name_plural = 'Блоки статьи'


class Comparison(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)

    # Модели для сравнения
    model1_name = models.CharField(max_length=100, verbose_name="Название первой модели")
    cover1 = models.ImageField(upload_to='comparisons/covers/', blank=True, null=True,
                               verbose_name="Обложка первой модели")
    model2_name = models.CharField(max_length=100, verbose_name="Название второй модели")
    cover2 = models.ImageField(upload_to='comparisons/covers/', blank=True, null=True,
                               verbose_name="Обложка второй модели")

    tags = models.ManyToManyField(Tag, related_name='comparisons', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model1_name} vs {self.model2_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сравнение'
        verbose_name_plural = 'Сравнения'


class ComparisonBlock(models.Model):
    HEADING_CHOICES = [
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
    ]

    IMAGE_SIZE_CHOICES = [
        ('original', 'Оригинальный'),
        ('square', 'Квадрат (1:1)'),
        ('vertical', 'Вертикальный (1:2)'),
        ('horizontal', 'Горизонтальный (2:1)'),
    ]

    TEXT_POSITION_CHOICES = [
        ('left', 'Слева'),
        ('right', 'Справа'),
    ]

    comparison = models.ForeignKey(Comparison, related_name='blocks', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    # Текстовые поля
    heading_type = models.CharField(max_length=5, choices=HEADING_CHOICES, blank=True)
    heading_text = models.CharField(max_length=200, blank=True)
    text_content = RichTextUploadingField(blank=True)
    text_position = models.CharField(max_length=10, choices=TEXT_POSITION_CHOICES, default='right')

    # Изображение
    image = models.ImageField(upload_to='comparisons/blocks/', blank=True, null=True)
    image_size = models.CharField(max_length=20, choices=IMAGE_SIZE_CHOICES, default='horizontal')
    image_alt_text = models.CharField(max_length=200, blank=True)
    image_title = models.CharField(max_length=200, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок сравнения'
        verbose_name_plural = 'Блоки сравнения'
