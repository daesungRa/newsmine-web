from django.urls import path

from apps.users import views as user_views


app_name = 'users'
urlpatterns = [
    path('login', user_views.LoginView.as_view(), name='login'),
    path('login/github', user_views.github_login, name='github-login'),
    path('login/github/callback', user_views.github_callback, name='github-callback'),
    path('login/kakao', user_views.kakao_login, name='kakao-login'),
    path('login/kakao/callback', user_views.kakao_callback, name='kakao-callback'),
    path('logout', user_views.logout, name='logout'),
    path('signup', user_views.SignUpView.as_view(), name='signup'),
    path('verify', user_views.wait_verification, name='wait-verification'),
    path('verify/<str:key>', user_views.complete_verification, name='complete-verification'),
]
