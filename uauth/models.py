from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import os
import uuid

# 이미지 리네임을 위한 함수 선언
# 원본 파일명을 그대로 저장하면 덮어쓰거나(충돌)/한글깨짐/사생활 노출 위험까지 날 수 있기 때문
def profile_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()   # .jpg, .png
    new_name = f'{uuid.uuid4().hex}{ext}'
    print('리네임명:', new_name)
    return f'profiles/{new_name}'

class UserDetail(models.Model):

    # related_name을 안쓰면 역참조 이름이 클래스이름을 소문자로 한 것이다.
    # user.userdetail과 같이 참조 가능
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)

    # pillow 라이브러리 설치 필요
    # 사용자가 올린 파일이 저장된 경로명이 저장될 속성

    # ImageField
    # 1. request.FILES를 받는 용도
    # 2. 파일을 로컬에 다운로드하는 용도
    # 3. 다운로드 받은 파일의 경로를 저장하는 용도
    # profile = models.ImageField(upload_to='profiles/', null=True, blank=True)
    profile = models.ImageField(upload_to=profile_upload_path, null=True, blank=True)

# UserCreationForm 상속: Django가 만들어 둔 비밀번호 검증을 그대로 활용(해싱 암호화 검증 관련)
class UserForm(UserCreationForm):

    # 필수 입력은 아님 
    # 다만 이후 이 form으로 save를 시킬 때 birthday과 profile은 form.cleaned_data에서 꺼내 UserDetail을 추가로
    # save() 해 주어야 한다.
    birthday = forms.DateField(label='Birthday', required=False)
    profile = forms.ImageField(label='Profile', required=False)

    # Meta: 이 폼이 어떤 모델의 어떤 필드를 다룰지 지정
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")