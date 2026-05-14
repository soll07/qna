from django.shortcuts import render, redirect
from .models import Question, Answer, QuestionForm
from django.http import Http404, HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    # N + 1 문제 발생(이후 답변 갯수만큼 추가 N개의 쿼리가 날아감)
    # questions = Question.objects.all().order_by('-created_at')  

    # N + 1 문제 해결(2번만 쿼리 날아감(단, 접근(question.answers 시마다 두번의 쿼리)))
    questions = Question.objects.prefetch_related('answers', 'author').order_by('-created_at')
    print(f'{questions = }')

    # 페이징 처리 

    # 1. 현재 페이지, page라는 변수로 쿼리스트링이 안넘어 오면 1
    page = request.GET.get('page', '1')  # 기본 페이지는 1페이지로 설정

    # 2. 전체 질문게시글 + 한번에 몇 개씩 볼껀지와 paging 처리 대상을 가지는 Paginator 객체 생성
    paginator = Paginator(questions, 10)

    # 3. 현재 페이지에 뿌려질 질문 10가지를 추출(마지막 페이지는 10개가 아닐 수 있음)
    page_obj = paginator.get_page(page)

    # return render(request, 'qna/index.html', {'questions': questions})
    return render(request, 'qna/index.html', {'page_obj': page_obj})

def question_detail(request, id):
    print(f'question_detail: {id}')
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        raise Http404(f'해당 질문이 존재하지 않습니다: {id}')
    return render(request, 'qna/question_detail.html', {'question': question})

# 답변 작성 페이지 가기전에 막을 수가 없어서 프론트에서 미리 js로 막아야 한다.
@login_required(login_url='uauth:login')
def answer_create(request, id):
    content = request.POST.get('content')
    print(f'{id = }')
    print(f'{content = }')

    # 1. question 객체 조회
    question = Question.objects.get(id=id)

    # 2. answer 객체 생성(insert 및 즉시 select)
    answer = Answer.objects.create(question=question, content=content, author=request.user)
    print(f'{id}번 질문에 {answer.id} 답변이 생성되었습니다.')

    # forward 대신 redirect로 수정
    # return render(request, 'qna/question_detail.html', {'question': question})
    return redirect('qna:question_detail', id=id)   # qna/questions/10와 같이 사용자의 url 요청 경로를 수정하고 재요청 시킴

def answer_delete(request, answer_id):
    
    # a태그는 무조건 GET 요청
    question_id = request.GET.get('question_id') # 쿼리스트링으로 넘어온 question_id 받아내기

    answer = Answer.objects.get(id=answer_id)
    print(f'{answer.id}번 답변이 삭제')
    answer.delete()

    return redirect('qna:question_detail', id=question_id)

# 이 핸들러 함수는 같은 경로로 오는 GET 요청 및 POST 요청을 모두 처리
# 1. (GET)question_form.html 렌더링
# 2. (POST)redirect -> 추가된 질문 상세페이지로

@login_required(login_url='uauth:login')
def question_create(request):
    print(request.method)
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            # question = form.save()   # insert 및 select 발생

            # 로그인 기능이 완성되고 나면 이제 작성자를 해당 게시글의 author로 등록 가능
            # request.user: 현재 로그인한 사람
            question = form.save(commit=False)  # 모델 객체만 반환하고 DB에 반영은 안한 상태
                                                # (subject 및 content만 들어있는 상태)
            question.author = request.user      # 현재 로그인한 사람을 author에 추가해서 
            question.save()        

            return redirect('qna:question_detail', id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'qna/question_form.html', {'form': form})

# messages 프레임워크 레벨
# : 리다이렉트 되는 페이지에 전달할 메세지를 담을 수 있다.
#   잠깐 담아뒀다가 페이지가 응답되면 소멸(내부적으로는 세션을 활용)
# - messages.success()
# - messages.error()
# - messages.warning()
# - messages.info()
@login_required(login_url='uauth:login')
def question_modify(request, id):
    
    # 오리지널 버전 조회
    question = Question.objects.get(id=id)

    if request.user != question.author and not request.user.is_staff:
        # return HttpResponseForbidden('수정 권한이 없습니다.')
        messages.error(request, '해당 질문 수정 권한이 없습니다.')
        return redirect('qna:question_detail', id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()    # 기존 Question 객체를 통해 update 발생
            messages.success(request, '해당 질문 수정 완료되었습니다.')
            return redirect('qna:question_detail', id=question.id)
    
    else:
        form = QuestionForm(instance=question)  # modify일 때는 기존에 작성된(조회된) 내용을 채운 form을 보냄

    return render(request, 'qna/question_form.html', {'form': form})

@login_required(login_url='uauth:login')
def question_delete(request, id):
    question = Question.objects.get(id=id)

    question.delete()
    return redirect('qna:index')  # 삭제 후 다시 목록보기로 이동

import json
from django.http import JsonResponse

@login_required(login_url='uauth:login')
def question_vote(request, id):

    # post 요청 시 request body에 담긴 걸 꺼내보는 간단 예제
    data = json.loads(request.body.decode('utf-8'))
    print(f'{data}')

    # 현재 요청을 날린 로그인한 유저가 해당 질문 게시글에 추천을 누르거나 해제하는 기능 작성
    question = Question.objects.get(id=id)

    if request.user == question.author:
        return JsonResponse(
            {'error': '본인이 작성한 게시글은 추천할 수 없습니다.'},
            status=403
        )

    # question.voters에 해당하는 중간 테이블에 현재 로그인한 회원이 추천한 적이 있는가
    if question.voters.filter(id=request.user.id).exists():

        # 있으면 제거
        question.voters.remove(request.user)
    else:

        # 없으면 추가
        question.voters.add(request.user)

    return JsonResponse({
        'vote_count': question.voters.count()
    })

@login_required(login_url='uauth:login')
def answer_vote(request, id):

    # 현재 요청을 날린 로그인한 유저가 해당 질문 게시글에 추천을 누르거나 해제하는 기능 작성
    answer = Answer.objects.get(id=id)

    if request.user == answer.author:
        return JsonResponse(
            {'error': '본인이 작성한 답변글은 추천할 수 없습니다.'},
            status=403
        )

    if answer.voters.filter(id=request.user.id).exists():

        # 있으면 제거
        answer.voters.remove(request.user)
    else:

        # 없으면 추가
        answer.voters.add(request.user)

    return JsonResponse({
        'vote_count': answer.voters.count()
    })