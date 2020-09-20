from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import HttpResponse, redirect
from django.template import Context
from django.template.loader import get_template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from post_service.forms import LoginForm
from post_service.models import Post
from user_manager.forms import JoinForm

# Create your views here.

def post_list(request):
    template = get_template('post_list.html')

    page_data = Paginator(Post.objects.all(), 5)
    page = request.GET.get('page')

    if page is None:
        page = 1

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    context = Context({'post_list': posts, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1)})

    return  HttpResponse(template.render(context))


def login(request):
    template = get_template('login_form.html')

    context = Context({'login_form': LoginForm()})
    context.update(csrf(request))

    return HttpResponse(template.render(context))

#로그인 처리 하는 함수
def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        user = auth.authenticate(username=login_form_data.cleaned_data['id'], password=login_form_data.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                request.session['username'] = login_form_data.cleaned_data['id']
                auth.login(request, user)

                return redirect('/board/')
        else:
            return HttpResponse('아이디/비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')

    return HttpResponse('알 수 없는 오류입니다.')

def join_page(request):
    if(request.method == 'POST'):
        form_data = JoinForm(request.POST)

        if form_data.is_valid():
            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']
            User.objects.create_user(username=username, password=password)

            return redirect('/user/login/')
    else:
        form_data = JoinForm()

    template = get_template('join_page.html')

    context = Context({'join_form': form_data})
    context.update(csrf(request))

    return HttpResponse(template.render(context))