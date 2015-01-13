from django.shortcuts import render

from zwiki.pages.models import Page, Category


def index(request, page_slug):
    page = Page.objects.get(slug__exact=page_slug)
    context = {
        'page': page
    }
    return render(request, 'pages/index.html', context)


def home(request):
    home_page = Page.objects.get(title__exact='Home')
    context = {
        'page': home_page,
    }
    return render(request, 'pages/index.html', context)
