from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *

# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    posts = Women.objects.filter(is_published=True)
    paginator=Paginator(posts,2)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context = {'cat_selected': 0,
               'page_obj':page_obj,
               'title': 'Главная страница'}
    return render(request, "women/index.html", context=context)


def about(request):
    posts=Women.objects.all()
    paginator=Paginator(posts,5)

    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    return render(request, "women/about.html", {"title": "About", "menu": menu, "page_obj":page_obj})


def add_page(request):

    if request.method == "POST":
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():
            # try:
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect("home")
            # except:
            #     form.add_error
            try:
                form.save()
                return redirect("home")
            except:
                form.add_error(None, "Ошибка добавления поста")

    else:
        form = AddPostForm()
    return render(request, "women/addpage.html", {"title": "Add page","form":form})


def contact(request):
    return render(request, "women/others.html", {"title": "Contact"})


def login(request):
    return render(request, "women/others.html", {"title": "Login"})


def get_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {"info": post,
               "title": post.title,
               "cat_selected": post.category_id}
    return render(request, 'women/info.html', context=context)


def show_categories(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(category_id=cat.id, is_published=True)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,
               'cat_selected': cat.id,
               'title': cat.name}
    return render(request, "women/index.html", context=context)


def categories(request, num):
    if num > 60:
        raise Http404()
    return HttpResponse(f"<h1>The different categories  {num} </h1>")


def slag_try(req, num_1, slug):
    return HttpResponse(f"<h1>Hello it is try page!!!</h1>"
                        f"<p>This is int first: {num_1} </p>"
                        f"<p>This is slug second : {slug} </p>")


def param(request):
    res = request.GET
    print(res)
    if res:
        return HttpResponse(f"<h2>Hello it is param page!!!</h2>"
                            f"<p>This is first param :  {res[list(res.keys())[0]]}</p>"
                            f"<p>This is second param : {res[list(res.keys())[1]]}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h3>Mistace 404 !!! Sorry not found</h3>")
