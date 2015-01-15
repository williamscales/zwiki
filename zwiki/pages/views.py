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
    """Retrieve and update the page.
        GET: Responds with a JSON representation of the Page object which can be
            fed to a viewmodels.js:PageViewModel
        PUT: Updates the Page with the submitted JSON data.

    """
    if request.method == 'GET':
        page = Page.objects.values().get(slug__exact=page_slug)
        return respond_with_json(json.dumps(page, default=json_serial))

    elif request.method == 'PUT':
        put = json.loads(request.body.decode(encoding='UTF-8'))
        page = Page.objects.get(slug__exact=put['slug'])
        page_history = PageHistory(title=page.title, date_published=page.date_published,
                                   edit_summary=page.edit_summary,
                                   content=page.content, public=page.public,
                                   author=page.author)
        page_history.page = page
        for category in page.categories.all():
            page_history.categories.add(category)
        page_history.save()
        page.title = put['title']
        page.edit_summary = put['edit_summary']
        page.date_published = datetime.now()
        page.content = put['content']
        page.save()
        return respond_with_json(json.dumps(page, default=json_serial))


def page_history(request, page_slug):
    """Query the page history.

    Responds with a JSON list of PageHistory objects corresponding to the
    desired page.

    """
    page = Page.objects.get(slug__exact=page_slug)
    page_history_list = list(page.page_history.all().values())
    return respond_with_json(json.dumps(page_history_list, default=json_serial))


def status(request, page_slug):
    """Query and update the lock status of the page.

        GET: Responds with { 'status': status_message }, where `status_message`
                is one of the following:
            * unlocked: the page is not locked and can be locked
            * locked: the page has recently been locked by someone else and
                cannot be locked again
            * owned: the page has recently been locked by the current user and
                can be edited safely
            * expired: the page was locked by the current user but the lock has
                expired and can be claimed by anyone.

        PUT: Accepts { 'status': desired_status } where `desired_status` is one
                of the following:
            * locked: indicates that the user wants to lock the page for editing
            * unlocked: indicates that the user wants to release the lock on the page
            Responds with { 'status': status_message } where `status_message` is
            as defined above.

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


def respond_with_json(j):
    """Utility function to quickly spit out a JSON response."""
    return HttpResponse(j, content_type='application/json')


def status_response(status, message=None):
    """Utility function to quickly generate a lock status response."""
    response = {'state': status}
    if message is not None:
        response['message'] = message
    return respond_with_json(json.dumps(response))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
