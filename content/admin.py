# content/admin.py
from django.contrib import admin
from .models import Tag, Article, ArticleBlock, Comparison, ComparisonBlock


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ArticleBlockInline(admin.StackedInline):
    model = ArticleBlock
    extra = 1
    fieldsets = (
        ('Порядок', {
            'fields': ('order',)
        }),
        ('Текстовый блок', {
            'fields': ('heading_type', 'heading_text', 'text_content', 'text_position')
        }),
        ('Изображение', {
            'fields': ('image', 'image_size', 'image_alt_text', 'image_title', 'image_caption')
        }),
    )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at', 'tags']
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    inlines = [ArticleBlockInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'excerpt', 'cover', 'category', 'tags', 'is_published')
        }),
        ('SEO настройки', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )


class ComparisonBlockInline(admin.StackedInline):
    model = ComparisonBlock
    extra = 1
    fieldsets = (
        ('Порядок', {
            'fields': ('order',)
        }),
        ('Текстовый блок', {
            'fields': ('heading_type', 'heading_text', 'text_content', 'text_position')
        }),
        ('Изображение', {
            'fields': ('image', 'image_size', 'image_alt_text', 'image_title', 'image_caption')
        }),
    )


class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('title', 'model1_name', 'model2_name', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'model1_name', 'model2_name', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [ComparisonBlockInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'excerpt', 'is_published', 'tags')
        }),
        ('Модели для сравнения', {
            'fields': ('model1_name', 'cover1', 'model2_name', 'cover2')
        }),
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comparison, ComparisonAdmin)
