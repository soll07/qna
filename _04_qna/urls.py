"""
URL configuration for _04_qna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# 파일업로드 관련
from django.conf import settings
from django.conf.urls.static import static

# 루트(localhost:8000)로 오면 /qna로 리다이렉트
# permanent=False -> 302응답(임시 이동), 브라우저가 캐싱하지 않아 매번 다시 서버 요청(기본 설정) - 개발 시
# permanent=True -> 301응답(영구 이동), 브라우저가 캐싱해 다음부터 서버를 거치지 않음
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='qna/', permanent=False)),
    path('qna/', include('qna.urls'), name='index'),
    path('uauth/', include('uauth.urls'), name='index'),
]

# 실제 배포 환경에서는 NGINX를 통한 서빙을 하고 개발 시(DEBUG=TRUE)에는 현재와 같이 작성하면
# /media/ 접두사로 하게 된다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)