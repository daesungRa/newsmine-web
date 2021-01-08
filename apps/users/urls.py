from django.urls import path

from apps.users import views as user_views


app_name = 'users'
urlpatterns = [
    path('login', user_views.LoginView.as_view(), name='login'),
    path('logout', user_views.logout, name='logout'),
    path('signup', user_views.SignUpView.as_view(), name='signup'),
]
