from django.core.context_processors import csrf
from django.shortcuts import HttpResponse, redirect
from django.template import Context
from django.template.loader import get_template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

from app.models import ExampleDotCom

# Create your views here.

def img_list(request):
    template = get_template('img_list.html')

    page_data = Paginator(ExampleDotCom.objects.all(), 100)
    page = request.GET.get('page')

    if page is None:
        page = 1

    try:
        imgs = page_data.page(page)
    except PageNotAnInteger:
        imgs = page_data.page(1)
    except EmptyPage:
        imgs = page_data.page(page_data.num_pages)

    context = Context({'img_list':imgs, 'current_page':int(page), 'total_page': range(1, page_data.num_pages + 1)})
    context.update(csrf(request))

    return HttpResponse(template.render(context))
