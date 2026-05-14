from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .models import UserForm, UserDetail, User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.db import transaction
from django.http import JsonResponse

def logout(request):
    auth_logout(request)
    return redirect('qna:index')

# get 요청: 회원가입 페이지 제공
# post 요청: 회원 insert(auth_user + uauth_userdetail 테이블 각각에...)

# 1. 데코레이터 방식의 트랜잭션 처리: signup 함수 자체를 하나의 트랜잭션으로 본다.
# @transaction.atomic
def signup(request):
    if request.method == 'POST':
        # form = UserForm(request.POST)  # 넘어온 데이터 중 text 데이터만 받을 때
        form = UserForm(request.POST, request.FILES) # 넘어온 이진 데이터도 추가로 받을 때
        print('유효한지 확인:', form.is_valid())
        if form.is_valid():

            # 2. 컨텍스트 매니저 방식의 트랜잭션 처리: with절 안을 하나의 트랜잭션으로 본다.
            with transaction.atomic():
                # 1. UserForm을 통한 User save() -> auth_user에 insert
                user = form.save()  

                # 2. UserDetail의 create -> uauth_userdetail에 insert
                UserDetail.objects.create(
                    user=user,
                    birthday=form.cleaned_data.get('birthday'),
                    profile=form.cleaned_data.get('profile')
                )

            # 회원가입 성공(두 테이블에 insert 성공) 이후 바로 로그인 상태가 되도록 작성해 보기(선택)
            # authenticate: 평문(암호화 되기 전)과 암호화된 암호(db에 저장된)를 비교
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )

            # 로그인: 서버의 session에 인증된 user가 담김
            auth_login(request, user)

        return redirect('qna:index')
    else:
        form = UserForm()

    return render(request, 'uauth/signup.html', {'form': form})

def check_username(request):
    username = request.GET.get('username')  # 쿼리스트링 형태로 넘어온 사용자가 입력한 회원 아이디

    is_exists = User.objects.filter(username=username).exists() # 같은 회원이 있으면 true
    print(is_exists)

    if is_exists:
        return JsonResponse({'available': False, 'message': '이미 사용중인 아이디입니다.'})

    return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})