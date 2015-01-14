from datetime import datetime
import json

from django.http import HttpResponse, QueryDict
from django.core.serializers import serialize
from django.shortcuts import render

from zwiki.pages.models import Page, PageHistory
from zwiki.appsettings.models import Setting


def index(request):
    context = {}
    return render(request, 'pages/index.html', context)


def page(request, page_slug):
    if request.method == 'GET':
        page = Page.objects.get(slug__exact=page_slug)
        return respond_with_json(page.to_json())

    elif request.method == 'PUT':
        put = json.loads(request.body.decode(encoding='UTF-8'))
        page_history = PageHistory( date_published = page.date_published,
                                   edit_summary = page.edit_summary, content =
                                   page.content, public = page.public, author =
                                   page.author, categories = page.categories)
        page_history.page = page
        page_history.save()
        page = Page.objects.get(slug__exact=put['slug'])
        page.title = put['title']
        page.edit_summary = put['editSummary']
        page.date_published = datetime.now()
        page.content = put['content']
        page.save()
        return respond_with_json(page.to_json())


def status(request, page_slug):
    """ GET: { 'status': status_message }, where `status_message` is one of the following:
            * unlocked: the page is not locked and can be locked
            * locked: the page has recently been locked by someone else and cannot be locked again
            * owned: the page has recently been locked by the current user and can be edited safely
            * expired: the page was locked by the current user but the lock has expired and can be claimed by anyone.

    """
    STATUS_OWNED = 'owned'
    STATUS_UNLOCKED = 'unlocked'
    STATUS_LOCKED = 'locked'
    STATUS_EXPIRED = 'expired'
    STATUS_ERROR = 'error'

    page = Page.objects.get(slug__exact=page_slug)

    if request.method == 'GET':

        if page.lock_state == page.UNLOCKED:
            return status_response(STATUS_UNLOCKED)

        elif page.lock_state == page.LOCKED and page.lock_is_fresh():
            if request.user == page.lock_owner:
                return status_response(STATUS_OWNED)
            else:
                return status_response(STATUS_LOCKED)

        elif page.lock_state == page.LOCKED and not page.lock_is_fresh():
            if request.user == page.lock_owner:
                return status_response(STATUS_EXPIRED)
            else:
                return status_response(STATUS_UNLOCKED)

    elif request.method == 'PUT':
        put = json.loads(request.body.decode(encoding='UTF-8'))

        if put['state'] == STATUS_LOCKED:
            if page.lock_state == page.UNLOCKED:
                page.lock(request.user)
                return status_response(STATUS_OWNED);
            elif page.lock_state == page.LOCKED and page.lock_is_fresh():
                if request.user == page.lock_owner:
                    return status_response(STATUS_OWNED)
                else:
                    return status_response(STATUS_LOCKED)
            elif page.lock_state == page.LOCKED and not page.lock_is_fresh():
                page.lock(request.user)
                return status_response(STATUS_OWNED)

        elif put['state'] == STATUS_UNLOCKED:
            if page.lock_state == page.UNLOCKED:
                return status_response(STATUS_UNLOCKED)
            if page.lock_state == page.LOCKED and page.lock_is_fresh():
                if request.user == page.lock_owner:
                    page.unlock()
                    return status_response(STATUS_UNLOCKED)
                else:
                    return status_response(STATUS_LOCKED)
            elif (page.lock_state == page.LOCKED and not page.lock_is_fresh()):
                page.unlock()
                return status_response(STATUS_UNLOCKED)

    return status_response(STATUS_ERROR, message=serialize('json', [page]))


def respond_with_json(x):
    return HttpResponse(x, content_type='application/json')


def status_response(status, message=None):
    response = {'state': status}
    if message is not None:
        response['message'] = message
    return respond_with_json(json.dumps(response))
