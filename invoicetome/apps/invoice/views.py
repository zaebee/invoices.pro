# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import translation
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import check_for_language
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import Invoice


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    data = {'invoice': invoice}

    if request.is_ajax():
        return render(request, 'includes/_invoice_detail.html', data)
    else:
        return render(request, 'invoice/invoice_detail.html', data)


def set_language(request):
    nextU = request.REQUEST.get('next', None)
    if not nextU:
        nextU = request.META.get('HTTP_REFERER', None)
    if not nextU:
        nextU = '/'
    response = HttpResponseRedirect(nextU)
    if request.method == 'GET':
        lang_code = request.GET.get('lang', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            translation.activate(lang_code)
            request.session.modified = True
    return response
