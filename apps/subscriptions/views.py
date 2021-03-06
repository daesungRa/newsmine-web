from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

from django.views.generic import DetailView, View
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.contrib.auth.models import AnonymousUser
from apps.subscriptions.models import Subscription as SubscriptionModel

from apps.subscriptions.forms import SubscriptionForm


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
    return render(request, 'apps/subscriptions/list.html', {
        'context': 'subscriptions',
        'subscriptions': list(subscriptions)
    })


class SubscriptionDetail(DetailView):
    """
    Subscription Detail.
    Instead of SubscriptionView's GET method.
    """
    model = SubscriptionModel
    template_name = 'apps/subscriptions/detail.html'


class SubscriptionView(View):
    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            # Return json response for modal
            return JsonResponse(data={'redirect_uri': 'subscriptions'})
        return render(request, 'apps/subscriptions/detail.html', {'form': form})

    def put(self, request):
        pass

    def delete(self, request):
        pass
