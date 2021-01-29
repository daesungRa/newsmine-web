from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from apps.subscriptions.models import Subscription as SubscriptionModel
from django.contrib.auth.models import AnonymousUser


class SubscriptionDetail(DetailView):
    """Subscription Detail"""
    model = SubscriptionModel
    template_name = 'subscriptions/detail.html'


def subscription_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 5)

    # Get subscriptions by request user info
    if isinstance(request.user, AnonymousUser):
        messages.add_message(request, messages.INFO, 'Please log in first.')
        return redirect(reverse('core:home'))
    else:
        subscriptions = SubscriptionModel.objects.filter(owner=request.user.id)

    if not subscriptions:
        messages.add_message(request, messages.INFO, 'Subscription does not exist.')
    else:
        # TODO: Add returning logic of subscriptions by page
        paginator = Paginator(subscriptions, page_size)
        subscription_page = paginator.page(int(page))
    return render(request, 'apps/subscriptions/list.html', {'subscriptions': list(subscriptions)})
