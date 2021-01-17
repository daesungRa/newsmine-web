from django.urls import path

from apps.users import views as user_views


app_name = 'users'
urlpatterns = [
    path('login', user_views.LoginView.as_view(), name='login'),
    path('login/github', user_views.github_login, name='github-login'),
    path('login/github/callback', user_views.github_callback, name='github-callback'),
    path('logout', user_views.logout, name='logout'),
    path('signup', user_views.SignUpView.as_view(), name='signup'),
    path('verify/<str:key>', user_views.complete_verification, name='complete-verification')
]
