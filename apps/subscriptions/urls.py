from django.urls import path

from apps.subscriptions import views as subscription_views


app_name = 'subscriptions'
urlpatterns = [
    path('', subscription_views.subscription_list, name='list'),
    path('<int:pk>', subscription_views.SubscriptionDetail.as_view(), name='detail'),
]
