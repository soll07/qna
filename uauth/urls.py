from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'uauth'

urlpatterns = [

    # 앱의 기본 views 대신 LoginView.as_view가 제공하는 뷰를 쓰면 로그인 페이지 뿐 아니라 로그인 처리까지 해준다.
    path('login/', auth_views.LoginView.as_view(template_name='uauth/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('check_username/', views.check_username, name='check_username'),
]