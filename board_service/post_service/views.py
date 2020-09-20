from django.core.context_processors import csrf
from django.shortcuts import HttpResponse, redirect
from django.template import Context
from django.template.loader import get_template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

from post_service.models import Post

# Create your views here.

def post_list(request):
    template = get_template('post_list.html')

    page_data = Paginator(Post.objects.order_by('-pk').all(), 5)
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
    context.update(csrf(request))

    return HttpResponse(template.render(context))

def update(request):
    template = get_template('post_update.html')
    title = request.POST.get('title')
    body = request.POST.get('body')
    pk = request.POST.get('pk')
    i = request.POST.get('del')

    if i == '삭제하기':
        pk = request.POST.get('pk')
        p = Post.objects.get(pk=pk)
        if p.author.username == request.session['username']:
            p.delete()
            return redirect('/board/')

        else:
            return HttpResponse('해당 게시물에 대한 권리가 없습니다!')

    context = Context({'index': 1, 'title': title, 'body': body, 'pk': pk})     #request.get_full_path를 이용하는게 더 깔끔할 듯
    context.update(csrf(request))

    return HttpResponse(template.render(context))

def detailed(request):
    template = get_template('post_detailed.html')
    key = request.GET.get('id')
    title = request.POST.get('title')
    body = request.POST.get('body')
    is_new = str(request.POST.get('is_new'))
    pk = str(request.POST.get('pk'))
    pk = pk.strip('/')

    if is_new == '1':
        user = User.objects.only('id').get(username=request.session['username'])
        p = Post(title=title, body=body, author=user, date=None )
        p.save()
        post = Post.objects.order_by().last()
    elif is_new == '0':
        p = Post.objects.get(pk=int(pk))
        if p.author.username == request.session['username']:
            p.title = title
            p.body = body
            p.save()
            post = Post.objects.get(pk=int(pk))
        else:
            return HttpResponse('해당 게시물에 대한 권리가 없습니다!')
    else:
        if key is None:
            return HttpResponse('요청하신 페이지가 존재하지 않습니다!')
        #게시글이 없는 경우, 예외처리 해야함!! 디비에 키가 없는것
        else:
            post = Post.objects.get(pk=key)

    context = Context({'post': post})
    context.update(csrf(request))

    return HttpResponse(template.render(context))

def create(request):
    template = get_template('post_update.html')
    context = Context({})
    context.update(csrf(request))

    return HttpResponse(template.render(context))