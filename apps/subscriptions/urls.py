from django.urls import path

from apps.subscriptions import views as subscription_views


app_name = 'subscriptions'
urlpatterns = [
    path('<int:pk>', subscription_views.SubscriptionDetail.as_view(), name='detail'),
    path('owner', subscription_views.subscriptions_by_owner, name='owner'),
]
