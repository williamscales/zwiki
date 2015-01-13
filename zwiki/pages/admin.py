from django.contrib import admin

from zwiki.pages.models import Page, PageHistory, Category


class CategoryInline(admin.TabularInline):
    model = Page.categories.through
    extra = 1


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Metadata', {'fields': ['public']}),
        ('Content', {'fields': ['edit_summary', 'title', 'content']}),
    ]
    list_display = ('title', 'date_published', 'edit_summary', 'author',
                    'public')
    inlines = [
        CategoryInline,
    ]


    def save_model(self, request, obj, form, change):
        obj.slug = obj.title.lower().replace(' ', '-')
        obj.author = request.user
        obj.save()

admin.site.register(Page, PageAdmin)
admin.site.register(Category)
