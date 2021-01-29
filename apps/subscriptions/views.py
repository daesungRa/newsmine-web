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


def subscriptions_by_owner(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 5)
    owner_id = request.GET.get('owner_id', None)
    try:
        owner_id = owner_id and int(owner_id)
    except ValueError:
        # TODO: Add error logger or messages
        owner_id = None

    # Filter by inserted owner or request user
    subscriptions = []
    if owner_id:
        subscriptions = SubscriptionModel.objects.filter(owner=owner_id)
    elif not isinstance(request.user, AnonymousUser):
        subscriptions = SubscriptionModel.objects.filter(owner=request.user.id)

    if not subscriptions:
        messages.add_message(request, messages.INFO, 'Subscription does not exist.')
        return redirect(reverse('core:home'))
    else:
        # TODO: Add returning logic of subscriptions by page
        paginator = Paginator(subscriptions, page_size)
        subscription_page = paginator.page(int(page))
